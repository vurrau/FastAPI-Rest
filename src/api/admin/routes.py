from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.user.model import User, UserRoleEnum
from src.api.user.schemas import UserRead
from src.services.manager import current_admin
from src.api.user.logic import update_employee_salary, update_user_role, get_employee_info
from src.core.db.base import get_async_session

admin = APIRouter(
    prefix="/admin",
    tags=["admin"]
)


@admin.get("/employee", response_model=list[UserRead])
async def get_full_info_employee(
        session: AsyncSession = Depends(get_async_session),
        current_user: User = Depends(current_admin)
):
    result = await get_employee_info(current_user, session)

    return result


@admin.patch("/role")
async def update_role(
        user_id: int,
        new_role: UserRoleEnum,
        session: AsyncSession = Depends(get_async_session),
        current_user: User = Depends(current_admin)
):
    result = await update_user_role(user_id, new_role, session)

    return result


@admin.patch("/salary")
async def update_salary(
        user_id: int,
        new_salary: int,
        session: AsyncSession = Depends(get_async_session),
        current_user: User = Depends(current_admin)
):
    result = await update_employee_salary(user_id, new_salary, session)

    return result
