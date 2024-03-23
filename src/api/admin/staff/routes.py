from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.user.logic import get_employee_info, get_user_info
from src.api.user.schemas import UserRead
from src.services.manager import current_employee
from src.api.user.model import User
from src.core.db.base import get_async_session

staff = APIRouter(
    prefix="/staff",
    tags=["staff"]
)


@staff.get("/employee", response_model=list[UserRead])
async def get_info_employee(
        session: AsyncSession = Depends(get_async_session),
        current_user: User = Depends(current_employee)
):
    result = await get_employee_info(current_user, session)

    return result


@staff.get("/user", response_model=list[UserRead])
async def get_info_user(
        session: AsyncSession = Depends(get_async_session),
        current_user: User = Depends(current_employee)
):
    result = await get_user_info(current_user, session)

    return result
