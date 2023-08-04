from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from settings import build_database_uri, build_engine_config, build_session_config

engine = create_async_engine(build_database_uri(), **build_engine_config())

SessionLocal = sessionmaker(
    engine, class_=AsyncSession, **build_session_config()
)  # type: ignore


async def get_session() -> AsyncGenerator:
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
