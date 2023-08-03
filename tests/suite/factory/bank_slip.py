from decimal import Decimal
from datetime import datetime, timedelta

import factory
from faker import Factory as FakerFactory

from chargeapi.db.models import DBBankSlip

faker = FakerFactory.create("pt_BR")


class DBBankSlipFactoryData(factory.Factory):
    class Meta:
        model = DBBankSlip

    id = factory.LazyFunction(lambda: faker.uuid4())
    code = "6A91AC74-D6BB-45CB-BC04-A6EB855A131B"
    payment_link = (
        "https://pagseguro.uol.com.br/checkout/print.jhtml?c=df0597592d53e100780"
    )
    barcode = "03399557345480000000998765401025954420000030050"
    paid_amount = Decimal('1000.00')
    paid_at = factory.LazyFunction(lambda: datetime.now() + timedelta(days=10))
    paid_by = factory.LazyFunction(lambda: faker.name())
    created_at = datetime.now()
    updated_at = datetime.now()
