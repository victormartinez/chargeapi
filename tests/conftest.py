import asyncio
from pathlib import Path

import pytest
import pytest_asyncio
from httpx import AsyncClient

from chargeapi.main import app

TESTS_FOLDER = Path(__file__).cwd() / "tests"


@pytest_asyncio.fixture
async def async_client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session")
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def bytes_reader():
    def callable(filename: str) -> str:
        filepath = TESTS_FOLDER / f"suite/data/{filename}"
        return filepath.read_bytes()

    return callable
