from datetime import date
from decimal import Decimal

from chargeapi.ext.bank_service import BankSlipService


async def test_bank_slip_service():
    service = BankSlipService(api_key="abcdef")
    assert service.api_key == "abcdef"

    document = await service.generate_bank_slip(
        "Harry Potter", "harry@hogwarts.com", Decimal("1000.0"), date(2023, 10, 21)
    )
    assert len(document.code) > 0
    assert (
        document.payment_link
        == "https://pagseguro.uol.com.br/checkout/payment/booklet/"
        f"print.jhtml?c={document.code}"
    )
    assert len(document.barcode) > 0
