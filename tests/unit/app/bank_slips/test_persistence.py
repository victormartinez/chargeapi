from datetime import date
from unittest import mock

from chargeapi.app.bank_slips import persist, BankSlipIn


async def test_persist():
    mock_session = mock.AsyncMock()
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
    await persist(mock_session, bank_slips)

    mock_session.bulk_save_objects.assert_called_once()
    mock_session.commit.assert_called_once()

