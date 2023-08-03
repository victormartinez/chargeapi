from datetime import date
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel


class DebtIn(BaseModel):
    name: str
    government_id: str
    email: str
    debt_amount: Decimal
    debt_due_date: date
    debt_identifier: str


class DebtOut(BaseModel):
    id: UUID
    name: str
    government_id: str
    email: str
    debt_amount: Decimal
    debt_due_date: date
    debt_identifier: str
