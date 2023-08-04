import asyncio
from typing import List

import structlog
from sqlalchemy.ext.asyncio import AsyncSession

from chargeapi.app.bank_slips import create_bank_slip
from chargeapi.app.debts.data import DebtOut
from chargeapi.app.debts.data.repository import ListDebtsWithoutBankSlipsRepository
from chargeapi.db.session import get_session

logger = structlog.get_logger("main")


async def create_bank_slips(session: AsyncSession, debts: List[DebtOut]) -> None:
    background_tasks = set()
    for item in debts:
        task = asyncio.create_task(
            create_bank_slip(
                session,
                item.id,
                item.name,
                item.email,
                item.debt_amount,
                item.debt_due_date,
            )
        )
        background_tasks.add(task)
        task.add_done_callback(background_tasks.discard)
    await asyncio.gather(*background_tasks)


async def process() -> None:
    has_next = True
    OFFSET, LIMIT, PAGE_SIZE = 0, 10, 10

    async for session in get_session():
        while has_next:
            repository = ListDebtsWithoutBankSlipsRepository(session)
            total, debts = await repository.execute(OFFSET, LIMIT)
            if total == 0 or len(debts) == 0:
                has_next = False

            await create_bank_slips(session, debts)
            OFFSET += PAGE_SIZE
