from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel


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
