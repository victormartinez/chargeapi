from typing import List, Sequence, Tuple

from sqlalchemy import func, select

from chargeapi.db.base_repository import BaseRepository
from chargeapi.db.models import DBBankSlip, DBDebt

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
                debt_identifier=bank_slip.debt_identifier,
            )
            for bank_slip in bank_slips
        ]
        await self.db_session.run_sync(
            lambda session: session.bulk_save_objects(objects)
        )
        await self.db_session.commit()


class ListDebtsRepository(BaseRepository):
    async def _adapt(self, db_bank_slips: Sequence[DBDebt]) -> List[DebtOut]:
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

    async def execute(self, offset: int, limit: int) -> List[DebtOut]:  # type: ignore
        query = select(DBDebt).offset(offset).limit(limit)
        query_result = await self.db_session.execute(query)
        db_rows: Sequence[DebtOut] = query_result.scalars().all()
        return await self._adapt(db_rows)


class ListDebtsWithoutBankSlipsRepository(BaseRepository):
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

    async def execute(self, offset: int, limit: int) -> Tuple[int, List[DebtOut]]:  # type: ignore
        query = (
            select(DBDebt, func.count(DBDebt.id).over())  # type: ignore
            .join(DBBankSlip, isouter=True)
            .where(DBBankSlip.id.is_(None))
            .order_by(DBDebt.debt_due_date.asc())
            .offset(offset)
            .limit(limit)
        )
        result = await self.db_session.execute(query)
        rows = result.all()
        if not rows:
            return 0, []

        total_items = rows[0][1]
        objects = [row[0] for row in rows]
        return total_items, await self._adapt(objects)
