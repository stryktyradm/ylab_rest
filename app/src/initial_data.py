import asyncio
import logging

from src.db.init_db import init_db
from src.db.session import async_session

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def init() -> None:
    async with async_session() as db:
        await init_db(db)


async def main() -> None:
    logger.info('Creating initial data')
    await init()
    logger.info('Initial data created')


if __name__ == '__main__':
    asyncio.run(main())
