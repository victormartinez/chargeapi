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


class BankSlipOut(BaseModel):
    id: UUID
    debt_id: UUID
    code: str
    payment_link: str
    barcode: str
    paid_at: Optional[datetime] = None
    paid_amount: Optional[Decimal] = None
    paid_by: Optional[str] = None
