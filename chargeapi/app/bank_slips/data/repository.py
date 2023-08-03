from typing import List

from sqlalchemy import update, select
from sqlalchemy.orm import joinedload

from chargeapi.app.exceptions import ChargeApiException, ChargeApiExceptionType
from chargeapi.app.bank_slips.data.entities import BankSlipPaymentIn, BankSlipOut
from chargeapi.db.base_repository import BaseRepository
from chargeapi.db.models import DBDebt, DBBankSlip



class RegisterBankSlipPaymentRepository(BaseRepository):
    async def execute(self, payment: BankSlipPaymentIn) -> bool:  # type: ignore
        query = (
            select(DBDebt)
            .join(DBBankSlip, isouter=True)
            .where(DBDebt.debt_identifier == payment.debt_identifier)
            .options(joinedload(DBDebt.bank_slip))
        )
        result = await self.db_session.execute(query)
        db_debt = result.scalars().first()
        if not db_debt:
            raise ChargeApiException(
                type=ChargeApiExceptionType.ENTITY_NOT_FOUND,
                message=f"Debt identifier #{payment.debt_identifier} not found"
            )
        
        db_bank_slip: DBBankSlip = db_debt.bank_slip
        if not db_bank_slip:
            raise ChargeApiException(
                type=ChargeApiExceptionType.ENTITY_NOT_FOUND,
                message=f"Debt identifier #{payment.debt_identifier} not found"
            )

        if db_bank_slip and db_bank_slip.paid_at:
            # Idempotency
            return True

        db_bank_slip.paid_at = payment.paid_at
        db_bank_slip.paid_amount = payment.paid_amount
        db_bank_slip.paid_by = payment.paid_by
        await self.db_session.commit()
        return True


class ListBankSlipsRepository(BaseRepository):

    async def _adapt(self, db_bank_slips: List[DBBankSlip]) -> List[BankSlipOut]:
        return [
            BankSlipOut(
                id=db_obj.id,
                debt_id=db_obj.debt_id,
                code=db_obj.code,
                payment_link=db_obj.payment_link,
                barcode=db_obj.barcode,
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
