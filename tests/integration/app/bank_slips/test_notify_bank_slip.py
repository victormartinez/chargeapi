from datetime import datetime
from decimal import Decimal

import pytest

from chargeapi.app.bank_slips import notify_bank_slip
from chargeapi.app.bank_slips.data import (
    BankSlipPaymentIn,
    ListNotNotifiedBankSlipDebtsRepository,
    RegisterBankSlipPaymentRepository,
    GetBankSlipRepository,
)
from tests.suite.database import DatabaseUtils
from tests.suite.factory import DBDebtFactoryData, DBBankSlipFactoryData


async def test_notify_bank_slip(session):
    db_debt = DBDebtFactoryData.build()
    await DatabaseUtils.create(session, db_debt)

    db_bank_slip = DBBankSlipFactoryData.build(debt_id=db_debt.id, notified_at=None)
    await DatabaseUtils.create(session, db_bank_slip)

    repository = ListNotNotifiedBankSlipDebtsRepository(session)
    total, bank_slips = await repository.execute(0, 10)
    assert total == 1
    
    has_notified = await notify_bank_slip(session, bank_slips[0])
    assert has_notified is True

    repo = GetBankSlipRepository(session)
    refreshed_obj = await repo.execute(bank_slips[0].id)
    assert refreshed_obj.notified_at is not None
    