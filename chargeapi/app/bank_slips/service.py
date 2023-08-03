import codecs
import csv
from datetime import datetime
from decimal import Decimal
from typing import BinaryIO

from sqlalchemy.ext.asyncio import AsyncSession

from chargeapi.app.exceptions import ChargeApiException, ChargeApiExceptionType
from chargeapi.app.bank_slips.data import (
    BankSlipIn, 
    BankSlipPaymentIn,   
    PersistBankSlipsRepository,
    RegisterBankSlipPaymentRepository,
)
from infrastructure import logging

CSV_CHARSET = "utf-8"


logger = logging.get_logger(__name__)


async def load_csv(session: AsyncSession, file: BinaryIO) -> None:
    logger.info("parsing csv")
    csv_reader = csv.DictReader(codecs.iterdecode(file, CSV_CHARSET))
    bank_slips = [
        BankSlipIn(
            name=row["name"].strip(),
            government_id=row["governmentId"].strip(),
            email=row["email"].strip(),
            debt_amount=Decimal(row["debtAmount"].strip()),
            debt_due_date=row["debtDueDate"].strip(),
            debt_id=row["debtId"].strip(),
        )
        for row in csv_reader
        if row
    ]

    logger.info("parsed bank slips", total=len(bank_slips))
    repository = PersistBankSlipsRepository(session)
    await repository.execute(bank_slips)
    logger.info("persisted bank slips")


async def register_payment(
    session: AsyncSession, 
    debt_id: str, 
    paid_at: datetime, 
    paid_amount: Decimal, 
    paid_by: str
) -> None:
    payment_in = BankSlipPaymentIn(
        debt_id=debt_id, paid_at=paid_at, paid_amount=paid_amount, paid_by=paid_by
    )
    repository = RegisterBankSlipPaymentRepository(session)
    updated = await repository.execute(payment=payment_in)
    if not updated:
        raise ChargeApiException(
            type=ChargeApiExceptionType.ENTITY_NOT_FOUND,
            message=f"Debt {debt_id} not found."
        )
    