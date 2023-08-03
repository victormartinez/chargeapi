from datetime import datetime, date
from decimal import Decimal
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

import settings
from chargeapi.ext.bank_service import BankSlipService
from chargeapi.ext.email_service import EmailApiClient
from chargeapi.app.exceptions import ChargeApiException, ChargeApiExceptionType
from chargeapi.app.bank_slips.data import (
    BankSlip,
    BankSlipPaymentIn,
    CreateBankSlipRepository,
    RegisterBankSlipPaymentRepository,
    FlagNotifiedBankSlipRepository,
)
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
    updated = await repository.execute(payment=payment_in)
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
    bank_slip_service = BankSlipService(api_key=settings.BANK_SLIP_API_KEY)
    bank_slip = await bank_slip_service.generate_bank_slip(
        name, email, debt_amount, debt_due_date
    )
    repository = CreateBankSlipRepository(session)
    return await repository.execute(
        debt_id, bank_slip.code, bank_slip.payment_link, bank_slip.barcode
    )


async def notify_bank_slip(
    session: AsyncSession,
    bank_slip: BankSlip,
) -> bool:
    email_client = EmailApiClient(api_key=settings.EMAIL_SERVICE_API_KEY)
    has_notified = await email_client.notify_bank_slip(
        bank_slip.code, bank_slip.payment_link, bank_slip.barcode
    )
    if has_notified:
        repository = FlagNotifiedBankSlipRepository(session)
        updated_row = await repository.execute(bank_slip.id)
        return bool(updated_row)
    return False
