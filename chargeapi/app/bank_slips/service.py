from datetime import datetime
from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession

from chargeapi.app.exceptions import ChargeApiException, ChargeApiExceptionType
from chargeapi.app.bank_slips.data import (
    BankSlipPaymentIn,   
    RegisterBankSlipPaymentRepository,
)
from infrastructure import logging

CSV_CHARSET = "utf-8"


logger = logging.get_logger(__name__)


async def register_payment(
    session: AsyncSession, 
    debt_identifier: str, 
    paid_at: datetime, 
    paid_amount: Decimal, 
    paid_by: str
) -> None:
    logger.info("started registering bank slip payment", debt_identifier=debt_identifier)
    payment_in = BankSlipPaymentIn(
        debt_identifier=debt_identifier, paid_at=paid_at, paid_amount=paid_amount, paid_by=paid_by
    )
    repository = RegisterBankSlipPaymentRepository(session)
    updated = await repository.execute(payment=payment_in)
    if not updated:
        logger.error("debt not found", debt_identifier=debt_identifier)
        raise ChargeApiException(
            type=ChargeApiExceptionType.ENTITY_NOT_FOUND,
            message=f"Debt {debt_identifier} not found."
        )
    logger.info("finished registering bank slip payment", debt_identifier=debt_identifier)
