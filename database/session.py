from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from . import Base
from config import DB_NAME, DB_PASSWORD, DB_PORT, DB_HOST, DB_USER

url = f'postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

# class AsyncDatabaseSession:
#     def __init__(self):
#         self._engine = None
#         self._session = None

#     def __getattr__(self, name):
#         return getattr(self._session, name)

#     async def init(self):
#         print('INITIALIZING DATABASE')
#         url = f'postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
#         # self._engine = create_async_engine(url)
#         self._engine = create_async_engine(url, echo=True)
#         self._session = sessionmaker(
#             self._engine, expire_on_commit=False, class_=AsyncSession
#         )()
#         async with self._engine.begin() as conn:
#             print(Base.metadata.tables.keys())
#             await conn.run_sync(Base.metadata.create_all)

#     async def close_connections(self):
#         await self._engine.dispose()


# async_db_session: AsyncSession = AsyncDatabaseSession()


engine = create_async_engine(url, echo=True)
connection = sessionmaker(engine, autocommit=False, autoflush=False, class_=AsyncSession)


async def get_session():
    try:
        session = connection()
        yield session
    finally:
        await session.close()


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def close_connections():
    await engine.dispose()
