from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.models import User, UserRoleEnum
from src.services.manager import fastapi_users
from src.services.utils import get_user_id
from src.core.db.base import get_async_session

admin = APIRouter(
    prefix="/admin",
    tags=["admin"]
)

current_superuser = fastapi_users.current_user(active=True, superuser=True)


@admin.get("/staff")
async def get_staff_full_info(
        session: AsyncSession = Depends(get_async_session),
        current_user: User = Depends(current_superuser)):
    query = select(User.email, User.name, User.salary, User.id, User.role).where(User.role != "USER")
    result = await session.execute(query)
    return result.mappings().all()


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

    query = select(User.email, User.name, User.salary, User.id, User.role).filter(User.id == user_id)
    result = await session.execute(query)

    await session.commit()

    return result.mappings().first()


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

    query = select(User.email, User.name, User.salary, User.id, User.role).filter(User.id == user_id)
    result = await session.execute(query)

    await session.commit()

    return result.mappings().all()