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


@admin.get("/employee", response_model=list[EmployeeInfo])
async def get_full_info_employee(current_user: User = Depends(current_admin)):
    result = await UserService.get_employee_info()

    return result


@admin.patch("/role", response_model=EmployeeInfo)
async def update_role(
        user_id: int,
        new_role: UserRoleEnum,
        current_user: User = Depends(current_admin)
):
    result = await UserService.update_user_role(user_id, new_role)

    return result


@admin.patch("/salary", response_model=EmployeeInfo)
async def update_salary(
        user_id: int,
        new_salary: int,
        current_user: User = Depends(current_admin)
):
    result = await UserService.update_employee_salary(user_id, new_salary)

    return result
