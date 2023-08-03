from datetime import datetime, date
from decimal import Decimal
from typing import Optional
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
    paid_at: Optional[datetime] = None
    paid_amount: Optional[Decimal] = None
    paid_by: Optional[str] = None
    notified_at: Optional[datetime] = None


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
    paid_at: Optional[datetime] = None
    paid_amount: Optional[Decimal] = None
    paid_by: Optional[str] = None
    notified_at: Optional[datetime] = None