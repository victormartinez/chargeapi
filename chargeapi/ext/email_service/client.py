from pydantic import BaseModel


class EmailApiResponse(BaseModel):
    code: str
    payment_link: str
    barcode: str


class EmailApiClient:
    def __init__(self, api_key: str):
        self.api_key = api_key

    async def notify_bank_slip(
        self, code: str, payment_link: str, barcode: str
    ) -> bool:
        return EmailApiResponse(
            code=code,
            payment_link=payment_link,
            barcode=barcode,
        )
