import pytest_asyncio
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm.session import sessionmaker

from chargeapi.db.models import (
    DBBankSlipDebt,
)
from chargeapi.db.session import SessionLocal
from chargeapi.main import app
from settings import build_database_uri, build_engine_config, build_session_config

engine = create_async_engine(build_database_uri(), **build_engine_config())
TestingSessionLocal = sessionmaker(
    engine, class_=AsyncSession, **build_session_config()
)


@pytest_asyncio.fixture(scope="function")
async def db(override_async_session):
    app.dependency_overrides[SessionLocal] = override_async_session

    yield override_async_session


@pytest_asyncio.fixture(scope="function", autouse=True)
async def clean_db(db):
    await db.execute(delete(DBBankSlipDebt))
    await db.commit()


@pytest_asyncio.fixture()
async def override_async_session():
    db = TestingSessionLocal()
    try:
        yield db
        await db.commit()
    finally:
        await db.close()
