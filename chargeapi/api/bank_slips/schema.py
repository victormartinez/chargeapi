from decimal import Decimal
from datetime import datetime
from pydantic import BaseModel, Field


class BankSlipPaymentInput(BaseModel):
    debt_id: str = Field(alias='debtId')
    paid_at: datetime = Field(alias='paidAt')
    paid_amount: Decimal  = Field(alias='paidAmount') # FIXME: should not be float
    paid_by: str = Field(alias='paidBy')
