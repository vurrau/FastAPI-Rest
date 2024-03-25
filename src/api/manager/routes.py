from fastapi import APIRouter, Depends

from src.api.user.model import User, UserRoleEnum
from src.api.employee.schemas import EmployeeInfoFull
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
        current_user: User = Depends(current_manager)
):
    result = await UserService.update_user_role(user_id, new_role)

    return result


@manager.patch("/salary", response_model=EmployeeInfoFull)
async def update_salary(
        user_id: int,
        new_salary: int,
        current_user: User = Depends(current_manager)
):
    result = await UserService.update_employee_salary(user_id, new_salary)

    return result
