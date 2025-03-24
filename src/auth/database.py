from src.database import engine, get_async_session

from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(SQLAlchemyBaseUserTableUUID, Base):
    pass


async def create_db_and_tables():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)
