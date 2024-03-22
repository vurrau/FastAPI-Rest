from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.user.logic import get_user_info, get_employee_info
from src.api.user.model import User
from src.core.db.base import get_async_session

user = APIRouter(
    prefix="/user",
    tags=["user"]
)


@user.get("/employee")
async def get_name_employee(session: AsyncSession = Depends(get_async_session)):
    info = await get_employee_info(None, session)

    return info


@user.get("/")
async def get_info_user(session: AsyncSession = Depends(get_async_session)):
    info = await get_user_info(None, session)

    return info
