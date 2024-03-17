from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.user.logic import get_employee_info, get_user_info
from src.services.manager import fastapi_users
from src.api.user.model import User
from src.core.db.base import get_async_session

staff = APIRouter(
    prefix="/staff",
    tags=["staff"]
)

current_staff = fastapi_users.current_user(active=True, verified=True)


@staff.get("/")
async def get_info_employee(
        session: AsyncSession = Depends(get_async_session),
        current_user: User = Depends(current_staff)
):
    info = await get_employee_info(current_user, session)

    return info


@staff.get("/user")
async def get_info_user(
        session: AsyncSession = Depends(get_async_session),
        current_user: User = Depends(current_staff)
):
    info = await get_user_info(current_user, session)

    return info
