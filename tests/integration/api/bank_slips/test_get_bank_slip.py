from http import HTTPStatus

from tests.suite.database import DatabaseUtils
from tests.suite.factory import DBBankSlipFactoryData, DBDebtFactoryData


async def test_get_bank_slip(session, async_client):
    db_debt = DBDebtFactoryData.build(debt_identifier="12356")
    await DatabaseUtils.create(session, db_debt)
    db_bank_slip = DBBankSlipFactoryData.build(debt_id=db_debt.id)
    await DatabaseUtils.create(session, db_bank_slip)

    response = await async_client.get(f"/bankslips/{db_bank_slip.id}")
    assert response.status_code == HTTPStatus.OK
    body = response.json()

    assert body["id"] == str(db_bank_slip.id)
    assert body["debt_id"] == str(db_debt.id)
    assert body["code"] == db_bank_slip.code
    assert body["payment_link"] == db_bank_slip.payment_link
    assert body["barcode"] == db_bank_slip.barcode
    assert body["paid_at"] == db_bank_slip.paid_at.isoformat()
    assert body["paid_amount"] == str(db_bank_slip.paid_amount)
    assert body["paid_by"] == db_bank_slip.paid_by
    assert body["notified_at"] == db_bank_slip.notified_at.isoformat()


async def test_register_bank_slip_payment_not_found(async_client):
    FAKE_ID = "9543c230-225b-48a0-bfd8-ef9fbadab4a6"
    response = await async_client.get(f"/bankslips/{FAKE_ID}")
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {
        "message": "Bank Slip (9543c230-225b-48a0-bfd8-ef9fbadab4a6) not found",
        "type": "ENTITY_NOT_FOUND",
        "code": 404,
        "errors": [],
    }
