from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.user.logic import get_user_info
from src.services.manager import fastapi_users
from src.api.user.model import User
from src.core.db.base import get_async_session

staff = APIRouter(
    prefix="/staff",
    tags=["staff"]
)

current_verified = fastapi_users.current_user(active=True, verified=True)


@staff.get("/")
async def get_staff_info(
        session: AsyncSession = Depends(get_async_session),
        current_user: User = Depends(current_verified)):

    info = await get_user_info(current_user, session)

    return info


@staff.get("/user")
async def get_user_name(
        session: AsyncSession = Depends(get_async_session),
        current_user: User = Depends(current_verified)):
    query = select(User.id, User.name).where(User.role == "USER")
    result = await session.execute(query)
    return result.mappings().all()

