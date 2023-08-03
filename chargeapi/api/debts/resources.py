from http import HTTPStatus

from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from chargeapi.app import debts
from chargeapi.db.session import get_session

router = APIRouter(tags=["debts"])


@router.post("/debts/ingest", status_code=HTTPStatus.CREATED, response_model=None)
async def ingest_debts(
    file: UploadFile, session: AsyncSession = Depends(get_session)
) -> None:
    await debts.load_csv(session, file.file)
