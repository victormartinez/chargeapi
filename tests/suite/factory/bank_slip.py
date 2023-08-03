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
    name = factory.LazyFunction(lambda: faker.name())
    government_id = factory.LazyFunction(lambda: str(faker.uuid4()))
    email  = factory.LazyFunction(lambda: faker.email())
    debt_due_date = factory.LazyFunction(lambda: datetime.now() + timedelta(days=20))
    debt_id = factory.LazyFunction(lambda: str(faker.uuid4()))
    debt_amount = Decimal('1000.00')
    paid_amount = Decimal('1000.00')
    paid_at = factory.LazyFunction(lambda: datetime.now() + timedelta(days=10))
    paid_by = factory.LazyFunction(lambda: faker.name())
    created_at = datetime.now()
    updated_at = datetime.now()
