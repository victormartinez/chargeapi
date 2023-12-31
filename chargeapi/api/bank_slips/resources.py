from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from chargeapi.api.bank_slips.schema import BankSlipPaymentInput
from chargeapi.app import bank_slips
from chargeapi.db.session import get_session

from .schema import BankSlipOut

router = APIRouter(tags=["bank_slips"])


@router.patch("/bankslips/pay", status_code=HTTPStatus.OK)
async def register_bank_slip_payment(
    payload: BankSlipPaymentInput, session: AsyncSession = Depends(get_session)
) -> None:
    await bank_slips.register_payment(
        session,
        debt_identifier=payload.debt_identifier,
        paid_at=payload.paid_at,
        paid_amount=payload.paid_amount,
        paid_by=payload.paid_by,
    )


@router.get("/bankslips/{idx}", status_code=HTTPStatus.OK, response_model=BankSlipOut)
async def retrieve_bank_slip(
    idx: UUID, session: AsyncSession = Depends(get_session)
) -> BankSlipOut:
    obj = await bank_slips.retrieve_bank_slip(session, idx)
    return BankSlipOut(**obj.model_dump())
