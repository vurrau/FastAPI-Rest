from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.user.logic import get_user_info
from src.api.user.model import User
from src.core.db.base import get_async_session

user = APIRouter(
    prefix="/user",
    tags=["user"]
)


@user.get("/staff")
async def get_staff_name(session: AsyncSession = Depends(get_async_session)):

    info = await get_user_info(None, session)
    return info


