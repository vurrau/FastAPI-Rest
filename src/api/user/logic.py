from fastapi import HTTPException

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.user.model import User, UserRoleEnum
from src.core.db.base import async_session_maker


class UserService:
    @staticmethod
    async def get_user_id(user_id: int):
        async with async_session_maker() as session:

            result = await session.execute(select(User).filter(User.id == user_id))
            return result.scalar_one_or_none()

    @staticmethod
    async def get_user_email(email: str):
        async with async_session_maker() as session:

            result = await session.execute(select(User).filter(User.email == email))
            return result.scalar_one_or_none()

    @staticmethod
    async def get_email_employee():
        async with async_session_maker() as session:
            roles = [UserRoleEnum.STAFF, UserRoleEnum.MANAGER]

            result = await session.execute(select(User.email).filter(User.role.in_(roles)))
            return result.scalars().all()

    @staticmethod
    async def get_employee_info():
        async with async_session_maker() as session:

            result = await session.execute(select(User).filter(User.role != UserRoleEnum.USER))
            return result.scalars().all()

    @staticmethod
    async def get_user_info():
        async with async_session_maker() as session:

            result = await session.execute(select(User).filter(User.role == UserRoleEnum.USER))
            return result.scalars().all()

    @staticmethod
    async def update_employee_salary(user_id: int, new_salary: int):
        async with async_session_maker() as session:

            user = await UserService.get_user_id(user_id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            if user.role == UserRoleEnum.USER:
                raise HTTPException(status_code=403, detail="User is not an employee")

            user.salary = new_salary

            session.add(user)
            await session.commit()
            return user

    @staticmethod
    async def update_user_role(user_id: int, new_role: UserRoleEnum):
        async with async_session_maker() as session:

            user = await UserService.get_user_id(user_id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")

            user.role = new_role
            user.is_verified = True

            if user.role == UserRoleEnum.USER:
                user.salary = 0
                user.is_verified = False

            session.add(user)
            await session.commit()
            return user


