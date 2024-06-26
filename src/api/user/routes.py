from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.user.logic import UserService
from src.api.user.model import User
from src.api.user.schemas import UserInfo, UserInfoBasic
from src.core.db.base import get_async_session
from src.services.manager import current_employee

user = APIRouter(
    prefix="/user",
    tags=["user"]
)


@user.get("/info", response_model=list[UserInfo])
async def get_info_user(session: AsyncSession = Depends(get_async_session)):
    result = await UserService.get_user_info(session)

    return result


@user.get("/info/basic", response_model=list[UserInfoBasic])
async def get_info_user_for_employee(current_user: User = Depends(current_employee),
                                     session: AsyncSession = Depends(get_async_session)):
    result = await UserService.get_user_info(session)

    return result


