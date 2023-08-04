import random
import string
from datetime import date
from decimal import Decimal
from urllib.parse import urljoin

from pydantic import BaseModel

import settings


class BankSlipDocument(BaseModel):
    code: str
    payment_link: str
    barcode: str


class BankSlipService:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = settings.BANK_SLIP_HOST

    async def generate_bank_slip(
        self, name: str, email: str, amount: Decimal, due_date: date
    ) -> BankSlipDocument:
        CODE_LENGTH, BARCODE_LENGTH = 64, 80
        code = "".join(
            random.choice(  # nosec
                string.ascii_uppercase + string.ascii_lowercase + string.digits
            )
            for _ in range(CODE_LENGTH)
        )
        barcode = "".join(
            random.choice(string.digits) for _ in range(BARCODE_LENGTH)  # nosec
        )

        payment_link = urljoin(
            self.base_url, f"/checkout/payment/booklet/print.jhtml?c={code}"
        )
        return BankSlipDocument(
            code=code,
            payment_link=payment_link,
            barcode=barcode,
        )
