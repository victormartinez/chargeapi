import io
from datetime import date
from unittest import mock

from chargeapi.app.bank_slips import load_csv, BankSlipIn


async def test_session_persist(bytes_reader):
    mock_session = mock.AsyncMock()
    await load_csv(mock_session, io.BytesIO(bytes_reader('bank_slip.csv')))

    mock_session.run_sync.assert_called_once()
    mock_session.commit.assert_called_once()


@mock.patch("chargeapi.app.bank_slips.service.PersistBankSlipsRepository.execute")
async def test_repository_persist(repo_execute_mock, bytes_reader):
    mock_session = mock.AsyncMock()
    await load_csv(mock_session, io.BytesIO(bytes_reader('bank_slip.csv')))

    repo_execute_mock.assert_called_once_with([
        BankSlipIn(
            name='John Doe',
            government_id='11111111111',
            email='johndoe@kanastra.com.br',
            debt_amount='1000000.00',
            debt_due_date=date(2022, 10, 12),
            debt_id='8291'
        )
    ])
