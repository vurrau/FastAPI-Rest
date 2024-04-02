from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.user.model import User, UserRoleEnum
from src.api.employee.schemas import EmployeeInfoFull
from src.core.db.base import get_async_session
from src.services.manager import current_manager
from src.api.user.logic import UserService

manager = APIRouter(
    prefix="/manager",
    tags=["manager"]
)


@manager.patch("/role", response_model=EmployeeInfoFull)
async def update_role(
        user_id: int,
        new_role: UserRoleEnum,
        current_user: User = Depends(current_manager),
        session: AsyncSession = Depends(get_async_session)
):
    result = await UserService.update_user_role(user_id, new_role, session)

    return result


@manager.patch("/salary", response_model=EmployeeInfoFull)
async def update_salary(
        user_id: int,
        new_salary: int,
        current_user: User = Depends(current_manager),
        session: AsyncSession = Depends(get_async_session)
):
    result = await UserService.update_employee_salary(user_id, new_salary, session)

    return result
