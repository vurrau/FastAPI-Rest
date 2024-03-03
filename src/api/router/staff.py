from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.manager import fastapi_users
from src.api.models import User
from src.db.base import get_async_session

staff = APIRouter(
    prefix="/staff",
    tags=["staff"]
)

current_verified = fastapi_users.current_user(active=True, verified=True)


@staff.get("/")
async def get_staff(
        session: AsyncSession = Depends(get_async_session),
        current_user: User = Depends(current_verified)):
    query = select(User.email, User.name, User.salary).where(User.role != "USER")
    result = await session.execute(query)
    return result.mappings().all()


@staff.get("/user")
async def get_user(
        session: AsyncSession = Depends(get_async_session),
        current_user: User = Depends(current_verified)):
    query = select(User).where(User.role == "USER")
    result = await session.execute(query)
    return result.scalars().all()

