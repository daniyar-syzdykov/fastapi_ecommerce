from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from database import Base
from config import TEST_DB_NAME, TEST_DB_PASSWORD, TEST_DB_PORT, TEST_DB_HOST, TEST_DB_USER


url = f'postgresql+asyncpg://{TEST_DB_USER}:{TEST_DB_PASSWORD}@{TEST_DB_HOST}:{TEST_DB_PORT}/{TEST_DB_NAME}'
engine = create_async_engine(url, echo=True)
connection = sessionmaker(engine, autocommit=False,
                          autoflush=False, class_=AsyncSession)

TABLES_CREATED = False


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def get_test_session():
    global TABLES_CREATED
    if not TABLES_CREATED:
        await create_tables()
        TABLES_CREATED = True
    try:
        session = connection()
        yield session
    finally:
        await session.close()
