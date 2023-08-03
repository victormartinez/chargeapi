import asyncio

from infrastructure import logging

logger = logging.get_logger(__name__)


async def process() -> None:
    logger.info("hello world")

    await asyncio.sleep(43200)
