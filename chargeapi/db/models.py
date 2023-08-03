# type: ignore
from sqlalchemy import DECIMAL, Column, Date, DateTime, ForeignKey, String
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import relationship

from chargeapi.db.base_model import BaseModel


class DBDebt(BaseModel):
    __tablename__ = "debts"

    name = Column(String, nullable=False)
    government_id = Column(String, nullable=False)
    email = Column(String, nullable=False)
    debt_amount = Column(DECIMAL, nullable=False)
    debt_due_date = Column(Date)
    debt_identifier = Column(String, nullable=False, unique=True, index=True)
    bank_slip = relationship("DBBankSlip", uselist=False)


class DBBankSlip(BaseModel):
    """
    Note:
        As the challenge allows abstracting details, this implementation takes some
        ideas from Pagbank API:
        https://dev.pagbank.uol.com.br/v1/reference/api-boleto-providers-gerar-boleto
    """

    __tablename__ = "bank_slips"

    debt_id = Column(
        postgresql.UUID(as_uuid=True),
        ForeignKey("debts.id"),
        nullable=False,
        unique=True,
    )
    code = Column(String, nullable=False)
    payment_link = Column(String, nullable=False)
    barcode = Column(String, nullable=False)
    paid_at = Column(DateTime, nullable=True)
    paid_amount = Column(DECIMAL, nullable=True)
    paid_by = Column(String, nullable=True)
    notified_at = Column(DateTime, nullable=True)
    debt = relationship("DBDebt", uselist=False)
