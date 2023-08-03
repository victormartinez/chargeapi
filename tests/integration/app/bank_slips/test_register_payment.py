from datetime import datetime
from decimal import Decimal

from chargeapi.app.bank_slips import load_csv
from chargeapi.app.bank_slips.data import (
    BankSlipPaymentIn,
    ListBankSlipsRepository,
    RegisterBankSlipPaymentRepository,
)
from tests.suite.database import DatabaseUtils
from tests.suite.factory.bank_slip import DBBankSlipFactoryData


async def test_register_payment(session):
    db_bank_slip = DBBankSlipFactoryData.build(
        debt_id="8291", paid_at=None, paid_amount=None, paid_by=None,
    )
    await DatabaseUtils.create(session, db_bank_slip)

    result = await ListBankSlipsRepository(session).execute()
    bank_slip = result[0]
    assert bank_slip.debt_id == "8291"
    assert bank_slip.paid_at is None
    assert bank_slip.paid_amount is None
    assert bank_slip.paid_by is None

    repo = RegisterBankSlipPaymentRepository(session)
    result = await repo.execute(
        BankSlipPaymentIn(
            debt_id="8291",
            paid_at=datetime.utcnow(),
            paid_amount=Decimal('1000.00'),
            paid_by="John Doe"
        )
    )
    assert result == 1

    result = await ListBankSlipsRepository(session).execute()
    bank_slip = result[0]
    assert bank_slip.debt_id == "8291"
    assert bank_slip.paid_at is not None
    assert bank_slip.paid_amount == Decimal('1000.00')
    assert bank_slip.paid_by == "John Doe"


async def test_register_payment_no_bank_slip(session):
    repo = RegisterBankSlipPaymentRepository(session)
    result = await repo.execute(
        BankSlipPaymentIn(
            debt_id="0987",
            paid_at=datetime.utcnow(),
            paid_amount=Decimal('1000.00'),
            paid_by="John Doe"
        )
    )
    assert result == 0
