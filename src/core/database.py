from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from typing import Generator

from src.core.configs import settings



engine: AsyncEngine = create_async_engine(settings.DB_URL)

Session: AsyncSession = sessionmaker(
    autocommit=False ,
    autoflush=False ,
    expire_on_commit=False ,
    class_=AsyncSession ,
    bind=engine
)


async def get_session() -> Generator:
    session: AsyncSession = Session()
    try:
        yield session
    finally:
        await session.close()


async def check_database_connection():
    session: AsyncSession = Session()
    try:
        await session.connection()
        await session.close()
        return True
    except Exception as error:
        print(error)
        return False
