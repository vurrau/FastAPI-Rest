from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.user.logic import UserService
from src.api.employee.schemas import EmployeeInfo, EmployeeInfoBasic, EmployeeInfoFull
from src.core.db.base import get_async_session
from src.services.manager import current_employee, current_manager
from src.api.user.model import User

employee = APIRouter(
    prefix="/employee",
    tags=["employee"]
)


@employee.get("/info", response_model=list[EmployeeInfo])
async def get_info_employee(session: AsyncSession = Depends(get_async_session)):
    result = await UserService.get_employee_info(session)

    return result


@employee.get("/info/basic", response_model=list[EmployeeInfoBasic])
async def get_info_employee_for_employee(current_user: User = Depends(current_employee),
                                         session: AsyncSession = Depends(get_async_session)):
    result = await UserService.get_employee_info(session)

    return result


@employee.get("/info/full", response_model=list[EmployeeInfoFull])
async def get_full_info_employee_for_manager(current_user: User = Depends(current_manager),
                                             session: AsyncSession = Depends(get_async_session)):
    result = await UserService.get_employee_info(session)

    return result



