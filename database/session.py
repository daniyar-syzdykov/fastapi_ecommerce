from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from . import Base
from config import settings

url = f'postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}'


engine = create_async_engine(url, echo=True)
connection = sessionmaker(engine, autocommit=False,
                          autoflush=False, class_=AsyncSession)


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
