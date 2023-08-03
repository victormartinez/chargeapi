from datetime import datetime
from decimal import Decimal

import pytest

from chargeapi.app.bank_slips.data import (
    BankSlipPaymentIn,
    ListBankSlipsRepository,
    RegisterBankSlipPaymentRepository,
)
from chargeapi.app.exceptions import ChargeApiException, ChargeApiExceptionType
from tests.suite.database import DatabaseUtils
from tests.suite.factory import DBBankSlipFactoryData, DBDebtFactoryData


async def test_register_payment(session):
    db_debt = DBDebtFactoryData.build(debt_identifier="8291")
    await DatabaseUtils.create(session, db_debt)
    db_bank_slip = DBBankSlipFactoryData.build(
        debt_id=db_debt.id, paid_amount=None, paid_at=None, paid_by=None
    )
    await DatabaseUtils.create(session, db_bank_slip)

    PAID_AT = datetime.utcnow()
    repo = RegisterBankSlipPaymentRepository(session)
    result = await repo.execute(
        BankSlipPaymentIn(
            debt_identifier="8291",
            paid_at=PAID_AT,
            paid_amount=Decimal("1000.00"),
            paid_by="John Doe",
        )
    )
    assert result is True

    bank_slips = await ListBankSlipsRepository(session).execute()
    assert len(bank_slips) == 1

    obj = bank_slips[0]
    assert obj.id is not None
    assert obj.debt_id is not None
    assert obj.code is not None
    assert obj.payment_link is not None
    assert obj.barcode is not None
    assert obj.paid_at == PAID_AT
    assert obj.paid_amount == Decimal("1000.00")
    assert obj.paid_by == "John Doe"


async def test_register_payment_no_bank_slip(session):
    repo = RegisterBankSlipPaymentRepository(session)

    with pytest.raises(ChargeApiException) as exc_info:
        await repo.execute(
            BankSlipPaymentIn(
                debt_identifier="0987",
                paid_at=datetime.utcnow(),
                paid_amount=Decimal("1000.00"),
                paid_by="John Doe",
            )
        )
    assert exc_info.value.type == ChargeApiExceptionType.ENTITY_NOT_FOUND
