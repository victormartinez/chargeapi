from datetime import date

from chargeapi.app.bank_slips import persist, BankSlipIn
from chargeapi.app.bank_slips.data.repository import ListBankSlipsRepository


async def test_persist(session):
    bank_slips = [
        BankSlipIn(
            name="John Doe",
            government_id="11111111111",
            email="johndoe@kanastra.com.br",
            debt_amount="1000000.00",
            debt_due_date=date(2022, 10, 12),
            debt_id="8291",
        )
    ]
    await persist(session, bank_slips)

    result = await ListBankSlipsRepository(session).execute()
    assert len(result) == 1
    bank_slip = result[0]
    assert bank_slip.id is not None
    assert bank_slip.name == "John Doe"
    assert bank_slip.government_id == "11111111111"
    assert bank_slip.email == "johndoe@kanastra.com.br"
    assert bank_slip.debt_amount == "1000000.00"
    assert bank_slip.debt_due_date == date(2022, 10, 12)
    assert bank_slip.debt_id == "8291"
