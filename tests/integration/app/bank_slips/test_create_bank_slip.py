from chargeapi.app.bank_slips import create_bank_slip
from chargeapi.db.models import DBDebt
from tests.suite.database import DatabaseUtils
from tests.suite.factory import DBDebtFactoryData


async def test_create_bank_slip(session):
    db_debt: DBDebt = DBDebtFactoryData.build(debt_identifier="6754")
    await DatabaseUtils.create(session, db_debt)

    result = await create_bank_slip(
        session,
        db_debt.id,
        db_debt.name,
        db_debt.email,
        db_debt.debt_amount,
        db_debt.debt_due_date,
    )
    assert result.id is not None
    assert str(result.debt_id) == str(db_debt.id)
    assert result.code is not None
    assert result.payment_link is not None
    assert result.barcode is not None
    assert result.paid_at is None
    assert result.paid_amount is None
    assert result.paid_by is None
