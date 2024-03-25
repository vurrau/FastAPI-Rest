from fastapi import APIRouter, Depends

from src.api.user.logic import UserService
from src.api.employee.schemas import EmployeeInfo, EmployeeInfoBasic, EmployeeInfoFull
from src.services.manager import current_employee, current_manager
from src.api.user.model import User

employee = APIRouter(
    prefix="/employee",
    tags=["employee"]
)


@employee.get("/info", response_model=list[EmployeeInfo])
async def get_info_employee():
    result = await UserService.get_employee_info()

    return result


@employee.get("/info/basic", response_model=list[EmployeeInfoBasic])
async def get_info_employee_for_employee(current_user: User = Depends(current_employee)):
    result = await UserService.get_employee_info()

    return result


@employee.get("/info/full", response_model=list[EmployeeInfoFull])
async def get_full_info_employee_for_manager(current_user: User = Depends(current_manager)):
    result = await UserService.get_employee_info()

    return result



