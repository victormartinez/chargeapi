from chargeapi.app.debts.data.repository import ListDebtsWithoutBankSlipsRepository
from tests.suite.database import DatabaseUtils
from tests.suite.factory import DBDebtFactoryData


async def test_list_debts_without_bank_slips_pagination(session):
    objects = DBDebtFactoryData.build_batch(10)
    await DatabaseUtils.create_many(session, objects)

    repository = ListDebtsWithoutBankSlipsRepository(session)
    total_items, result = await repository.execute(0, 4)
    assert total_items == 10
    assert len(result) == 4

    total_items, result = await repository.execute(4, 4)
    assert total_items == 10
    assert len(result) == 4

    total_items, result = await repository.execute(8, 4)
    assert total_items == 10
    assert len(result) == 2
