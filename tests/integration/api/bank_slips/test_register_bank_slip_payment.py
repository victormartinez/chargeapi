from http import HTTPStatus

from tests.suite.database import DatabaseUtils
from tests.suite.factory import DBBankSlipFactoryData, DBDebtFactoryData


async def test_register_bank_slip_payment_success(session, async_client):
    db_debt = DBDebtFactoryData.build(debt_identifier="12356")
    await DatabaseUtils.create(session, db_debt)
    db_bank_slip = DBBankSlipFactoryData.build(
        debt_id=db_debt.id, paid_amount=None, paid_at=None, paid_by=None
    )
    await DatabaseUtils.create(session, db_bank_slip)

    response = await async_client.patch(
        "/bankslips/pay",
        json={
            "debtId": "12356",
            "paidAt": "2022-06-09 10:00:00",
            "paidAmount": 100000.00,
            "paidBy": "John Doe",
        },
    )
    assert response.status_code == HTTPStatus.OK


async def test_register_bank_slip_payment_not_found(async_client):
    response = await async_client.patch(
        "/bankslips/pay",
        json={
            "debtId": "7648",
            "paidAt": "2022-06-09 10:00:00",
            "paidAmount": 100000.00,
            "paidBy": "John Doe",
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
