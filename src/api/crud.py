from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.models import User, UserRoleEnum
from src.api.manager import fastapi_users
from src.db.base import get_async_session

crud = APIRouter(
    prefix="/crud",
    tags=["crud"],
)

current_superuser = fastapi_users.current_user(active=True, superuser=True)


@crud.get("/users/protected/staff")
async def protected_route(
        session: AsyncSession = Depends(get_async_session),
        current_user: User = Depends(current_superuser)):
    query = select(User).where(User.role != "USER")
    result = await session.execute(query)
    return result.scalars().all()


@crud.get("/users/staff")
async def get_staff(session: AsyncSession = Depends(get_async_session)):
    query = select(User.name).where(User.role != "USER")
    result = await session.execute(query)
    return result.scalars().all()


@crud.put("/users/role")
async def update_user_role(
        user_id: int,
        new_role: UserRoleEnum,
        session: AsyncSession = Depends(get_async_session),
        current_user: User = Depends(current_superuser)
):
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="You do not have permission to perform this action")

    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.role = new_role
    await session.commit()

    return user
