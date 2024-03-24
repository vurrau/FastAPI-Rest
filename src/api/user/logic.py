from fastapi import HTTPException

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.user.model import User, UserRoleEnum
from src.core.db.base import get_async_session


class UserService:
    @staticmethod
    async def get_user_id(user_id: int, session: AsyncSession):
        result = await session.execute(select(User).filter(User.id == user_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_user_email(email: str, session: AsyncSession):
        result = await session.execute(select(User).filter(User.email == email))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_email_employee(session: AsyncSession):
        roles = [UserRoleEnum.STAFF, UserRoleEnum.MANAGER]

        result = await session.execute(select(User.email).filter(User.role.in_(roles)))
        return result.scalars().all()

    @staticmethod
    async def get_employee_info(session: AsyncSession, current_user: User = None):
        if current_user and current_user.is_superuser:
            query = select(User.email, User.name, User.salary, User.id, User.role).filter(
                User.role != UserRoleEnum.USER)

        elif current_user and current_user.is_verified:
            query = select(User.email, User.name, User.id, User.role).filter(User.role != UserRoleEnum.USER)

        else:
            query = select(User.email, User.name).filter(User.role != UserRoleEnum.USER)

        result = await session.execute(query)
        return result.mappings().all()

    @staticmethod
    async def update_employee_salary(user_id: int, new_salary: int, session: AsyncSession):
        user = await UserService.get_user_id(user_id, session)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if user.role == UserRoleEnum.USER:
            raise HTTPException(status_code=403, detail="User is not an employee")

        user.salary = new_salary
        await session.commit()
        return user

    @staticmethod
    async def update_user_role(user_id: int, new_role: UserRoleEnum, session: AsyncSession):
        user = await UserService.get_user_id(user_id, session)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        user.role = new_role
        user.is_verified = True

        if user.role == UserRoleEnum.USER:
            user.salary = 0
            user.is_verified = False

        await session.commit()
        return user

    @staticmethod
    async def get_user_info(session: AsyncSession, current_user: User = None):
        if current_user and current_user.is_verified:
            query = select(User.email, User.name, User.id).filter(User.role == UserRoleEnum.USER)
        else:
            query = select(User.name).filter(User.role == UserRoleEnum.USER)
        result = await session.execute(query)
        return result.mappings().all()
