from typing import List

import asyncio
import structlog
from sqlalchemy.ext.asyncio import AsyncSession

from chargeapi.db.session import get_session
from chargeapi.app.bank_slips import notify_bank_slip
from chargeapi.app.bank_slips.data import BankSlip
from chargeapi.app.bank_slips.data.repository import ListNotNotifiedBankSlipDebtsRepository


logger = structlog.get_logger("main")


async def notify(session: AsyncSession, bank_slips: List[BankSlip]):
    background_tasks = set()
    for item in bank_slips:
        task = asyncio.create_task(notify_bank_slip(session, item))
        background_tasks.add(task)
        task.add_done_callback(background_tasks.discard)
    return await asyncio.gather(*background_tasks)


async def process() -> None:
    has_next = True
    OFFSET, LIMIT, PAGE_SIZE = 0, 10, 10

    async for session in get_session():
        while has_next:
            repository = ListNotNotifiedBankSlipDebtsRepository(session)
            total, bank_slips = await repository.execute(OFFSET, LIMIT)
            if total == 0 or len(bank_slips) == 0:
                has_next = False

            await notify(session, bank_slips)
            OFFSET += PAGE_SIZE
