from sqlalchemy import DECIMAL, Column, DateTime, Date, String

from chargeapi.db.base_model import BaseModel


class DBBankSlip(BaseModel):
    __tablename__ = "bank_slips"

    name = Column(String, nullable=False)
    government_id = Column(String, nullable=False)
    email = Column(String, nullable=False)
    debt_amount = Column(DECIMAL, nullable=False)
    debt_due_date = Column(Date)
    debt_id = Column(String, nullable=False, unique=True, index=True)
    paid_at = Column(DateTime, nullable=True)
    paid_amount = Column(String, nullable=True)
    paid_by = Column(String, nullable=True)
