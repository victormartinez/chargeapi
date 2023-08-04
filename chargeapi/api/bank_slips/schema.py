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
        alias="debtId",
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
        alias="paidAmount",
    )  # FIXME: should not be float
    paid_by: str = Field(
        ...,
        title="Paid By",
        description="Specifies who paid the debt.",
        example="John Doe",
        alias="paidBy",
    )


class BankSlipOut(BaseModel):
    id: UUID = Field(
        ...,
        title="Bank slip ID",
        description="ID of a given bank slip.",
        example="9543c230-225b-48a0-bfd8-ef9fbadab4a6",
    )
    debt_id: UUID = Field(
        ...,
        title="Debt IT",
        description="ID of the related debt.",
        example="3d9f8e35-fd10-4dab-bd11-c4f3db90c0ad",
    )
    code: str = Field(
        ...,
        title="Bank Slip Code",
        description="Code that uniquely identifies the bank slip.",
        example="6A91AC74-D6BB-45CB-BC04-A6EB855A131B",
    )
    payment_link: str = Field(
        ...,
        title="Payment Link",
        description="Url that renders the bank slip",
        example="https://pagseguro.uol.com.br/checkout/print.jhtml?c=df0597592d53e",
    )
    barcode: str = Field(
        ...,
        title="Barcode",
        description="Barcode of bank slip",
        example="03399557345480000000998765401025954420000030050",
    )
    paid_at: datetime | None = Field(
        title="Paid At",
        description="Specifies when it was paid.",
        example="2023-10-01T12:30:44",
    )
    paid_amount: Decimal | None = Field(
        title="Paid Amount",
        description="Specifies how much was paid.",
        example=1231.21,
    )
    paid_by: str | None = Field(
        title="Paid By",
        description="Specifies who paid the debt.",
        example="John Doe",
    )
    notified_at: datetime | None = Field(
        title="Notified At",
        description="Specifies when the bank slip was sent.",
        example="2023-09-23T14:40:00",
    )
