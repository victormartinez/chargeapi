from http import HTTPStatus
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, UploadFile

from chargeapi.app import bank_slips
from chargeapi.db.session import get_session

router = APIRouter(tags=["bank_slips"])


@router.post("/bankslips/ingest", status_code=HTTPStatus.CREATED, response_model=None)
async def ingest_bank_slips(file: UploadFile, session: AsyncSession = Depends(get_session)) -> None:
    await bank_slips.load_csv(session, file.file)
