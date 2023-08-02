from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure import logging
from chargeapi.app.exceptions import (
    ChargeApiException,
    ChargeApiExceptionType,
)

from .data.repository import PersistBankSlipDebtsRepository

logger = logging.get_logger(__name__)


async def persist_bank_slip_debts(session: AsyncSession) -> bool:
    bind_logger = logger.bind()
    repository = await PersistBankSlipDebtsRepository(session)
