from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.models import User, UserRoleEnum
from src.api.manager import fastapi_users
from src.api.utils import get_user_id
from src.db.base import get_async_session

admin = APIRouter(
    prefix="/admin",
    tags=["admin"]
)

current_superuser = fastapi_users.current_user(active=True, superuser=True)


@admin.get("/staff")
async def get_staff_full_info(
        session: AsyncSession = Depends(get_async_session),
        current_user: User = Depends(current_superuser)):
    query = select(User).where(User.role != "USER")
    result = await session.execute(query)
    return result.scalars().all()


@admin.put("/role")
async def update_role(
        user_id: int,
        new_role: UserRoleEnum,
        session: AsyncSession = Depends(get_async_session),
        current_user: User = Depends(current_superuser)
):

    user = await get_user_id(user_id, session)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.role = new_role
    user.is_verified = True

    if user.role == UserRoleEnum.USER:
        user.salary = 0
        user.is_verified = False

    await session.commit()

    return user


@admin.put("/salary")
async def update_staff_salary(
        user_id: int,
        new_salary: int,
        session: AsyncSession = Depends(get_async_session),
        current_user: User = Depends(current_superuser)
):

    user = await get_user_id(user_id, session)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.role == UserRoleEnum.USER:
        raise HTTPException(status_code=409, detail="User is not staff")

    user.salary = new_salary

    await session.commit()

    return user
