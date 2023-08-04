from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field, NaiveDatetime


class BankSlipPaymentInput(BaseModel):
    debt_identifier: str = Field(
        ...,
        title="Debt identifier",
        description="Specifies the internal identifier of a given debt",
        example="8291",
        alias="debtId"
    )
    paid_at: NaiveDatetime = Field(
        ...,
        title="Paid Date",
        description="Specifies when the debt was paid.",
        example="2023-08-04T02:28:35",
        alias="paidAt",
    )
    paid_amount: Decimal = Field(
        ...,
        title="Paid Amount",
        description="Specifies the amount paid.",
        example=100.21,
        alias="paidAmount"
    )  # FIXME: should not be float
    paid_by: str = Field(
        ...,
        title="Paid By",
        description="Specifies who paid the debt.",
        example="John Doe",
        alias="paidBy",
    )


class BankSlipOut(BaseModel):
    id: UUID
    debt_id: UUID
    code: str
    payment_link: str
    barcode: str
    paid_at: datetime | None = None
    paid_amount: Decimal | None = None
    paid_by: str | None = None
    notified_at: datetime | None = None
