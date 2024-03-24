from typing import Optional, Any

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.user.logic import UserService
from src.api.staff.schemas import UserInfo, EmployeeInfo
from src.services.manager import current_employee
from src.api.user.model import User
from src.core.db.base import get_async_session

staff = APIRouter(
    prefix="/staff",
    tags=["staff"]
)


@staff.get("/employee", response_model=list[EmployeeInfo])
async def get_info_employee(current_user: User = Depends(current_employee)):
    result = await UserService.get_employee_info()

    return result


@staff.get("/user", response_model=list[UserInfo])
async def get_info_user(current_user: User = Depends(current_employee)):
    result = await UserService.get_user_info()

    return result
