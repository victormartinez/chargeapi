from abc import abstractmethod
from typing import Any

from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from chargeapi.app.exceptions import ChargeApiException, ChargeApiExceptionType


class BaseRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def run(self, *args: Any, **kwargs: Any):  # type: ignore
        try:
            return await self.execute(*args, **kwargs)
        except IntegrityError as exc:
            raise ChargeApiException(
                type=ChargeApiExceptionType.DATABASE_INTEGRITY_ERROR,
                message=str(exc),
            )
        except SQLAlchemyError as exc:
            raise ChargeApiException(
                type=ChargeApiExceptionType.DATABASE_ERROR, message=str(exc)
            )

    @abstractmethod
    async def execute(self, *args: Any, **kwargs: Any) -> Any:  # type: ignore
        pass
