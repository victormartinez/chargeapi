from typing import List

from sqlalchemy import and_, func, select
from sqlalchemy.orm import load_only

from chargeapi.db.base_repository import BaseRepository
from chargeapi.db.models import DBBankSlipDebt


class PersistBankSlipDebtsRepository(BaseRepository):
    async def execute(self) -> List[int]:  # type: ignore
        pass