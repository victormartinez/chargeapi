from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

import settings
from chargeapi.app.bank_slips.data import (
    BankSlip,
    BankSlipDebt,
    BankSlipPaymentIn,
    CreateBankSlipRepository,
    FlagNotifiedBankSlipRepository,
    GetBankSlipRepository,
    RegisterBankSlipPaymentRepository,
)
from chargeapi.app.exceptions import ChargeApiException, ChargeApiExceptionType
from chargeapi.ext.bank_service import BankSlipService
from chargeapi.ext.email_service import EmailApiClient
from infrastructure import logging

CSV_CHARSET = "utf-8"


logger = logging.get_logger(__name__)


async def register_payment(
    session: AsyncSession,
    debt_identifier: str,
    paid_at: datetime,
    paid_amount: Decimal,
    paid_by: str,
) -> None:
    logger.info(
        "started registering bank slip payment", debt_identifier=debt_identifier
    )
    payment_in = BankSlipPaymentIn(
        debt_identifier=debt_identifier,
        paid_at=paid_at,
        paid_amount=paid_amount,
        paid_by=paid_by,
    )
    repository = RegisterBankSlipPaymentRepository(session)
    updated = await repository.run(payment=payment_in)
    if not updated:
        logger.error("debt not found", debt_identifier=debt_identifier)
        raise ChargeApiException(
            type=ChargeApiExceptionType.ENTITY_NOT_FOUND,
            message=f"Debt {debt_identifier} not found.",
        )
    logger.info(
        "finished registering bank slip payment", debt_identifier=debt_identifier
    )


async def create_bank_slip(
    session: AsyncSession,
    debt_id: UUID,
    name: str,
    email: str,
    debt_amount: Decimal,
    debt_due_date: date,
) -> BankSlip:
    logger.info("started creating bank slip", debt_id=debt_id)
    bank_slip_service = BankSlipService(api_key=settings.BANK_SLIP_API_KEY)
    bank_slip = await bank_slip_service.generate_bank_slip(
        name, email, debt_amount, debt_due_date
    )
    repository = CreateBankSlipRepository(session)
    result = await repository.run(
        debt_id, bank_slip.code, bank_slip.payment_link, bank_slip.barcode
    )
    logger.info("finished creating bank slip", id=result.id, debt_id=debt_id)
    return result


async def notify_bank_slip(session: AsyncSession, bank_slip: BankSlipDebt) -> bool:
    logger.info("started notifying bank slip", debt_id=bank_slip.debt_id)
    email_client = EmailApiClient(api_key=settings.EMAIL_SERVICE_API_KEY)
    email_client.from_(settings.CONTACT_EMAIL)
    email_client.to(bank_slip.debt.email)
    email_client.subject("Boleto Bancário")
    email_client.body(f'''
        Olá, {bank_slip.debt.name}

        Boleto disponível em {bank_slip.payment_link}

        Código de barras: {bank_slip.barcode}
        ''')

    has_notified = await email_client.notify()
    if has_notified:
        repository = FlagNotifiedBankSlipRepository(session)
        updated_row = await repository.run(bank_slip.id)
        logger.info("notified bank slip", debt_id=bank_slip.debt_id)
        return bool(updated_row)

    logger.warning("did not notify bank slip", debt_id=bank_slip.debt_id)
    return False


async def retrieve_bank_slip(session: AsyncSession, idx: UUID) -> BankSlip:
    repo = GetBankSlipRepository(session)
    obj = await repo.run(idx)
    if not obj:
        raise ChargeApiException(
            type=ChargeApiExceptionType.ENTITY_NOT_FOUND,
            message=f"Bank Slip ({idx}) not found",
        )
    return obj
