from pydantic import BaseModel


class EmailApiResponse(BaseModel):
    to: str
    from_: str
    subject: str
    body: str


class EmailApiClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self._to = None
        self._from = None
        self._subject = None
        self._body = None

    def to(self, to: str) -> None:
        self._to = to

    def from_(self, from_: str) -> None:
        self._from = from_

    def subject(self, subject: str) -> None:
        self._subject = subject

    def body(self, body: str) -> None:
        self._body = body

    async def notify(self) -> bool:
        return EmailApiResponse(
            to=self._to,
            from_=self._from,
            subject=self._subject,
            body=self._body,
        )
