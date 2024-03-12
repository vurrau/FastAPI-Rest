from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.models import User
from src.core.db.base import get_async_session

user = APIRouter(
    prefix="/user",
    tags=["user"]
)


@user.get("/staff")
async def get_staff_name(session: AsyncSession = Depends(get_async_session)):
    query = select(User.name, User.role).where(User.role != "USER")
    result = await session.execute(query)
    return result.mappings().all()

