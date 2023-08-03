from datetime import date

import structlog


logger = structlog.get_logger("main")


async def process() -> None:
    today = date.today()

    logger.debug("hello world", today=today)

