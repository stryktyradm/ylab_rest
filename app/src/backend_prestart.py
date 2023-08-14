import asyncio
import logging

from sqlalchemy.sql import text
from src.db.cache import get_cache_connection
from src.db.session import async_session
from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

max_tries = 60 * 5
wait_seconds = 1


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
async def init() -> None:
    try:
        async with async_session() as db_session:
            await db_session.execute(text('SELECT 1'))
        cache = await get_cache_connection()
        await cache.info()
    except Exception as e:
        logger.error(e)
        raise e


async def main() -> None:
    logger.info('Initializing DB/Cache service')
    await init()
    logger.info('Service DB/Cache finished initializing')


if __name__ == '__main__':
    asyncio.run(main())
