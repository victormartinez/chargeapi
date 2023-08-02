from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure import logging
from chargeapi.app.bank_slips.data import BankSlipIn, PersistBankSlipsRepository


logger = logging.get_logger(__name__)


async def persist(session: AsyncSession, bank_slips: List[BankSlipIn]) -> bool:
    logger.info("persisting bank slips", total=len(bank_slips))
    repository = PersistBankSlipsRepository(session)
    await repository.execute(bank_slips)
    return True
