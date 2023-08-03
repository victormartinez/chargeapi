from typing import List, Optional

from sqlalchemy import select, update

from chargeapi.db.base_repository import BaseRepository
from chargeapi.db.models import DBBankSlip
from .entities import BankSlipIn, BankSlipOut, BankSlipPaymentIn


class PersistBankSlipsRepository(BaseRepository):

    async def execute(self, bank_slips: List[BankSlipIn]) -> None:  # type: ignore
        objects = [
            DBBankSlip(
                name=bank_slip.name,
                government_id=bank_slip.government_id,
                email=bank_slip.email,
                debt_amount=bank_slip.debt_amount,
                debt_due_date=bank_slip.debt_due_date,
                debt_id=bank_slip.debt_id
            ) 
            for bank_slip in bank_slips
        ]
        await self.db_session.run_sync(
            lambda session: session.bulk_save_objects(objects)
        )
        await self.db_session.commit()


class RegisterBankSlipPaymentRepository(BaseRepository):
    async def execute(self, payment: BankSlipPaymentIn) -> int:  # type: ignore
        query_update = (
            update(DBBankSlip)
            .where(DBBankSlip.debt_id == payment.debt_id)
            .values(
                paid_at=payment.paid_at,
                paid_amount=payment.paid_amount,
                paid_by=payment.paid_by,
            )
        )
        result = await self.db_session.execute(query_update)
        await self.db_session.commit()
        return result.rowcount


class ListBankSlipsRepository(BaseRepository):

    async def _adapt(self, db_bank_slips: List[DBBankSlip]) -> List[BankSlipOut]:
        return [
            BankSlipOut(
                id=db_obj.id,
                name=db_obj.name,
                government_id=db_obj.government_id,
                email=db_obj.email,
                debt_amount=db_obj.debt_amount,
                debt_due_date=db_obj.debt_due_date,
                debt_id=db_obj.debt_id,
                paid_at=db_obj.paid_at,
                paid_amount=db_obj.paid_amount,
                paid_by=db_obj.paid_by,
            ) 
            for db_obj in db_bank_slips
        ]

    async def execute(self) -> List[BankSlipOut]:  # type: ignore
        query = select(DBBankSlip)
        query_result = await self.db_session.execute(query)
        db_rows = query_result.scalars().all()
        return await self._adapt(db_rows)
