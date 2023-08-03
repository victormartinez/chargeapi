from datetime import date, datetime
from decimal import Decimal
from uuid import UUID
from typing import Optional

from pydantic import BaseModel


class BankSlipPaymentIn(BaseModel):
    debt_id: str 
    paid_at: datetime 
    paid_amount: Decimal 
    paid_by: str


class BankSlipIn(BaseModel):
    name: str
    government_id: str
    email: str
    debt_amount: Decimal
    debt_due_date: date
    debt_id: str


class BankSlipOut(BaseModel):
    id: UUID
    name: str
    government_id: str
    email: str
    debt_amount: Decimal
    debt_due_date: date
    debt_id: str
    paid_at: Optional[datetime] = None
    paid_amount: Optional[Decimal] = None
    paid_by: Optional[str] = None