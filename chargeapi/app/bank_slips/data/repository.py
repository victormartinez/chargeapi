from datetime import datetime
from uuid import UUID
from typing import List, Tuple

from sqlalchemy import select, update, func
from sqlalchemy.orm import joinedload

from chargeapi.app.exceptions import ChargeApiException, ChargeApiExceptionType
from chargeapi.app.bank_slips.data.entities import BankSlipPaymentIn, BankSlip
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
                message=f"Debt identifier #{payment.debt_identifier} not found",
            )

        db_bank_slip: DBBankSlip = db_debt.bank_slip
        if not db_bank_slip:
            raise ChargeApiException(
                type=ChargeApiExceptionType.ENTITY_NOT_FOUND,
                message=f"Debt identifier #{payment.debt_identifier} not found",
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
    async def _adapt(self, db_bank_slips: List[DBBankSlip]) -> List[BankSlip]:
        return [
            BankSlip(
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

    async def execute(self) -> List[BankSlip]:  # type: ignore
        query = select(DBBankSlip)
        query_result = await self.db_session.execute(query)
        db_rows = query_result.scalars().all()
        return await self._adapt(db_rows)


class CreateBankSlipRepository(BaseRepository):
    async def _adapt(self, db_bank_slips: List[DBBankSlip]) -> List[BankSlip]:
        return BankSlip(
            id=db_bank_slips.id,
            debt_id=db_bank_slips.debt_id,
            code=db_bank_slips.code,
            payment_link=db_bank_slips.payment_link,
            barcode=db_bank_slips.barcode,
        )

    async def execute(
        self, debt_id: UUID, code: str, payment_link: str, barcode: str
    ) -> BankSlip:
        db_bank_slip = DBBankSlip(
            debt_id=debt_id, code=code, payment_link=payment_link, barcode=barcode
        )
        self.db_session.add(db_bank_slip)
        await self.db_session.commit()
        await self.db_session.refresh(db_bank_slip, attribute_names=["id"])
        return await self._adapt(db_bank_slip)


class ListNotNotifiedBankSlipsRepository(BaseRepository):
    async def _adapt(self, db_bank_slips: List[DBBankSlip]) -> List[BankSlip]:
        return [
            BankSlip(
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

    async def execute(self, offset: int, limit: int) -> Tuple[int, List[BankSlip]]:
        query = (
            select(DBBankSlip, func.count(DBBankSlip.id).over())
            .where(DBBankSlip.notified_at.is_(None))
            .order_by(DBBankSlip.created_at.asc())
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


class FlagNotifiedBankSlipRepository(BaseRepository):
    async def execute(self, idx: UUID) -> int:
        query_update = (
            update(DBBankSlip)
            .where(DBBankSlip.id == idx)
            .values(notified_at=datetime.utcnow())
        )
        result = await self.db_session.execute(query_update)
        await self.db_session.commit()
        return result.rowcount
