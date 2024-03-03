from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.models import User
from src.db.base import get_async_session

user = APIRouter(
    prefix="/user",
    tags=["user"]
)


@user.get("/staff")
async def get_staff(session: AsyncSession = Depends(get_async_session)):
    query = select(User.name, User.role).where(User.role != "USER")
    result = await session.execute(query)
    return result.mappings().all()

