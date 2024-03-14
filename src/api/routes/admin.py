from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.user.model import User, UserRoleEnum
from src.services.manager import fastapi_users
from src.api.user.logic import get_user_id, update_user_salary, update_user_role, get_user_info
from src.core.db.base import get_async_session

admin = APIRouter(
    prefix="/admin",
    tags=["admin"]
)

current_superuser = fastapi_users.current_user(active=True, superuser=True)


@admin.get("/staff")
async def get_staff_full_info(
        session: AsyncSession = Depends(get_async_session),
        current_user: User = Depends(current_superuser)):

    info = await get_user_info(current_user, session)

    return info


@admin.put("/role")
async def update_role(
        user_id: int,
        new_role: UserRoleEnum,
        session: AsyncSession = Depends(get_async_session),
        current_user: User = Depends(current_superuser)
):

    updated_role = await update_user_role(user_id, new_role, session)

    return updated_role


@admin.put("/salary")
async def update_salary(
        user_id: int,
        new_salary: int,
        session: AsyncSession = Depends(get_async_session),
        current_user: User = Depends(current_superuser)
):

    updated_user = await update_user_salary(user_id, new_salary, session)

    return updated_user
