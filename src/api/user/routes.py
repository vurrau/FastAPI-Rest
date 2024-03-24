from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.user.logic import UserService
from src.api.user.schemas import UserInfo, EmployeeInfo
from src.core.db.base import get_async_session

user = APIRouter(
    prefix="/user",
    tags=["user"]
)


@user.get("/staff", response_model=list[EmployeeInfo])
async def get_name_employee(session: AsyncSession = Depends(get_async_session)):
    info = await UserService.get_employee_info(session)

    return info


@user.get("/", response_model=list[UserInfo])
async def get_info_user(session: AsyncSession = Depends(get_async_session)):
    info = await UserService.get_user_info(session)

    return info
