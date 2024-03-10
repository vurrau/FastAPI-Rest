from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import session

from src.api.models import User
from src.db.base import get_async_session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)


async def get_user_id(user_id: int, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


async def get_user_email(email: str, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()
