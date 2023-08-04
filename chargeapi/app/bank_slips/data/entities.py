from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel


class BankSlipPaymentIn(BaseModel):
    debt_identifier: str
    paid_at: datetime
    paid_amount: Decimal
    paid_by: str


class BankSlip(BaseModel):
    id: UUID
    debt_id: UUID
    code: str
    payment_link: str
    barcode: str
    paid_at: datetime | None = None
    paid_amount: Decimal | None = None
    paid_by: str | None = None
    notified_at: datetime | None = None


class Debt(BaseModel):
    id: UUID
    name: str
    government_id: str
    email: str
    debt_amount: Decimal
    debt_due_date: date
    debt_identifier: str


class BankSlipDebt(BaseModel):
    id: UUID
    debt_id: UUID
    debt: Debt
    code: str
    payment_link: str
    barcode: str
    paid_at: datetime | None = None
    paid_amount: Decimal | None = None
    paid_by: str | None = None
    notified_at: datetime | None = None
