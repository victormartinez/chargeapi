import codecs
import csv
from datetime import datetime
from decimal import Decimal
from typing import BinaryIO

from sqlalchemy.ext.asyncio import AsyncSession

from chargeapi.app.debts.data import DebtIn, PersistDebtRepository
from infrastructure import logging

CSV_CHARSET = "utf-8"
DATE_FORMAT = "%Y-%m-%d"

logger = logging.get_logger(__name__)


async def load_csv(session: AsyncSession, file: BinaryIO) -> None:
    logger.info("parsing csv")
    csv_reader = csv.DictReader(codecs.iterdecode(file, CSV_CHARSET))
    bank_slips = [
        DebtIn(
            name=row["name"].strip(),
            government_id=row["governmentId"].strip(),
            email=row["email"].strip(),
            debt_amount=Decimal(row["debtAmount"].strip()),
            debt_due_date=datetime.strptime(
                row["debtDueDate"].strip(), DATE_FORMAT
            ).date(),
            debt_identifier=row["debtId"].strip(),
        )
        for row in csv_reader
        if row
    ]

    logger.info("parsed csv", debts=len(bank_slips))
    repository = PersistDebtRepository(session)
    await repository.run(bank_slips)
    logger.info("persisted bank slips")
