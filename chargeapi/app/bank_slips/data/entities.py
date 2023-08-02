from datetime import date
from pydantic import BaseModel


class BankSlipIn(BaseModel):
    name: str
    government_id: str
    email: str
    debt_amount: str
    debt_due_date: date
    debt_id: str
