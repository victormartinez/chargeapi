from sqlalchemy import Column, Date, Integer, String

from chargeapi.db.base_model import BaseModel


class DBBankSlipDebt(BaseModel):
    __tablename__ = "bank_slip_debts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    government_id = Column(String, nullable=False)
    email = Column(String, nullable=False)
    debt_amount = Column(String, nullable=False)
    debt_due_date = Column(Date)
    debt_id = Column(String, nullable=False)
