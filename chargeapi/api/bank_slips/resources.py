from http import HTTPStatus
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, UploadFile

from chargeapi.app import bank_slips
from chargeapi.db.session import get_session
from .schema import BankSlipPaymentInput

router = APIRouter(tags=["bank_slips"])


@router.post("/bankslips/ingest", status_code=HTTPStatus.CREATED, response_model=None)
async def ingest_bank_slips(file: UploadFile, session: AsyncSession = Depends(get_session)) -> None:
    await bank_slips.load_csv(session, file.file)


@router.patch(
    "/bankslips/pay",
    status_code=HTTPStatus.OK
)
async def pay_bank_slip(payload: BankSlipPaymentInput, session: AsyncSession = Depends(get_session)) -> None:
    await bank_slips.register_payment(
        session, 
        debt_id=payload.debt_id,
        paid_at=payload.paid_at,
        paid_amount=payload.paid_amount,
        paid_by=payload.paid_by,
    )
