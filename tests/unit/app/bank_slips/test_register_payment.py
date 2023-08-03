import io
from decimal import Decimal
from datetime import datetime
from unittest import mock

from chargeapi.app.bank_slips import register_payment
from chargeapi.app.bank_slips.data import BankSlipPaymentIn


async def test_session_register_payment():
    mock_session = mock.AsyncMock()
    await register_payment(
        mock_session, "9827", datetime.utcnow(), Decimal("1000.00"), "John Doe"
    )

    mock_session.execute.assert_called_once()
    mock_session.commit.assert_called_once()


@mock.patch("chargeapi.app.bank_slips.service.RegisterBankSlipPaymentRepository.execute")
async def test_repository_register_payment(repo_execute_mock, bytes_reader):
    mock_session = mock.AsyncMock()
    UTC_NOW = datetime.utcnow()
    await register_payment(
        mock_session, "9827", UTC_NOW, Decimal("1000.00"), "John Doe"
    )

    repo_execute_mock.assert_called_once_with(
        payment=BankSlipPaymentIn(
            debt_id="9827",
            paid_at=UTC_NOW,
            paid_amount=Decimal("1000.00"),
            paid_by="John Doe"
        )
    )
