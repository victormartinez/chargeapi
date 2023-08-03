from datetime import date
from decimal import Decimal

from chargeapi.ext.email_service import EmailApiClient


async def test_bank_slip_service():
    service = EmailApiClient(api_key='abcdef')
    assert service.api_key == 'abcdef'

    response = await service.notify_bank_slip(
        code="1234",
        payment_link="https://payment?c=123456789",
        barcode="123456789",
    )
    assert response.code == "1234"
    assert response.payment_link == "https://payment?c=123456789"
    assert response.barcode == "123456789"
