from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field


class BankSlipPaymentInput(BaseModel):
    debt_identifier: str = Field(alias="debtId")
    paid_at: datetime = Field(alias="paidAt")
    paid_amount: Decimal = Field(alias="paidAmount")  # FIXME: should not be float
    paid_by: str = Field(alias="paidBy")


class BankSlipOut(BaseModel):
    id: UUID
    debt_id: UUID
    code: str
    payment_link: str
    barcode: str
    paid_at: datetime | None = None
    paid_amount: Decimal | None = None
    paid_by: str | None = None
    notified_at: datetime | None = None
