from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from database import Base
from config import TEST_DB_NAME, TEST_DB_PASSWORD, TEST_DB_PORT, TEST_DB_HOST, TEST_DB_USER


class AsyncDatabaseSession:
    def __init__(self):
        self._engine = None
        self._session = None

    def __getattr__(self, name):
        return getattr(self._session, name)

    async def init(self):
        url = f'postgresql+asyncpg://{TEST_DB_USER}:{TEST_DB_PASSWORD}@{TEST_DB_HOST}:{TEST_DB_PORT}/{TEST_DB_NAME}'
        # self._engine = create_async_engine(url)
        self._engine = create_async_engine(url, echo=True)
        self._session = sessionmaker(
            self._engine, expire_on_commit=False, class_=AsyncSession
        )()
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    async def close_connections(self):
        await self._engine.dispose()


test_async_db_session: AsyncSession = AsyncDatabaseSession()
