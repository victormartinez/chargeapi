from http import HTTPStatus
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends

from chargeapi.db.session import get_session

router = APIRouter(tags=["bank_slips"])


@router.post(
    "/charges/bankslips/load",
    status_code=HTTPStatus.CREATED
)
async def retrieve_facility(session: AsyncSession = Depends(get_session)) -> None:
    import pdb; pdb.set_trace()
    pass
