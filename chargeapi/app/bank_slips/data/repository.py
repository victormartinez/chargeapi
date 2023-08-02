from typing import List

from chargeapi.db.base_repository import BaseRepository
from chargeapi.db.models import DBBankSlip
from .entities import BankSlipIn


class PersistBankSlipsRepository(BaseRepository):
    async def execute(self, debts: List[BankSlipIn]) -> None:  # type: ignore
        objects = [
            DBBankSlip(
                name=debt.name,
                government_id=debt.government_id,
                email=debt.email,
                debt_amount=debt.debt_amount,
                debt_due_date=debt.debt_due_date,
                debt_id=debt.debt_id
            ) 
            for debt in debts
        ]
        await self.db_session.bulk_save_objects(objects)
        await self.db_session.commit()
