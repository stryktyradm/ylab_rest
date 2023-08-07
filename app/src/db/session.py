from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import AsyncAdaptedQueuePool
from src.core.config import settings

async_engine = create_async_engine(
    settings.SQLALCHEMY_DATABASE_URI, poolclass=AsyncAdaptedQueuePool, future=True
)
async_session = async_sessionmaker(async_engine, expire_on_commit=False)


async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session
