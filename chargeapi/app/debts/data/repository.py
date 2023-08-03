from typing import List

from sqlalchemy import select

from chargeapi.db.base_repository import BaseRepository
from chargeapi.db.models import DBDebt
from .entities import DebtIn, DebtOut


class PersistDebtRepository(BaseRepository):

    async def execute(self, bank_slips: List[DebtIn]) -> None:  # type: ignore
        objects = [
            DBDebt(
                name=bank_slip.name,
                government_id=bank_slip.government_id,
                email=bank_slip.email,
                debt_amount=bank_slip.debt_amount,
                debt_due_date=bank_slip.debt_due_date,
                debt_identifier=bank_slip.debt_identifier
            ) 
            for bank_slip in bank_slips
        ]
        await self.db_session.run_sync(
            lambda session: session.bulk_save_objects(objects)
        )
        await self.db_session.commit()


class ListDebtsRepository(BaseRepository):

    async def _adapt(self, db_bank_slips: List[DBDebt]) -> List[DebtOut]:
        return [
            DebtOut(
                id=db_obj.id,
                name=db_obj.name,
                government_id=db_obj.government_id,
                email=db_obj.email,
                debt_amount=db_obj.debt_amount,
                debt_due_date=db_obj.debt_due_date,
                debt_identifier=db_obj.debt_identifier,
            ) 
            for db_obj in db_bank_slips
        ]

    async def execute(self) -> List[DebtOut]:  # type: ignore
        query = select(DBDebt)
        query_result = await self.db_session.execute(query)
        db_rows = query_result.scalars().all()
        return await self._adapt(db_rows)
