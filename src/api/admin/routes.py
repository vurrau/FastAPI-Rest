from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.user.model import User, UserRoleEnum
from src.api.admin.schemas import EmployeeInfo
from src.services.manager import current_admin
from src.api.user.logic import UserService
from src.core.db.base import get_async_session

admin = APIRouter(
    prefix="/admin",
    tags=["admin"]
)

user_service = UserService()


@admin.get("/employee", response_model=list[EmployeeInfo])
async def get_full_info_employee(
        session: AsyncSession = Depends(get_async_session),
        current_user: User = Depends(current_admin)
):
    result = await user_service.get_employee_info(session, current_user)

    return result


@admin.patch("/role")
async def update_role(
        user_id: int,
        new_role: UserRoleEnum,
        session: AsyncSession = Depends(get_async_session),
        current_user: User = Depends(current_admin)
):
    result = await user_service.update_user_role(user_id, session, new_role, session)

    return result


@admin.patch("/salary")
async def update_salary(
        user_id: int,
        new_salary: int,
        session: AsyncSession = Depends(get_async_session),
        current_user: User = Depends(current_admin)
):
    result = await user_service.update_employee_salary(user_id, new_salary, session)

    return result
