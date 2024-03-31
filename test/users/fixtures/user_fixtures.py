import pytest
from passlib.context import CryptContext

from src.api.user.model import UserRoleEnum, User

context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@pytest.fixture
async def create_manager(session):
    async with session as async_session:
        user = User(
            email="liza@gmail.com",
            hashed_password=context.hash("12345"),
            name="Liza",
            salary=4000,
            role=UserRoleEnum.MANAGER,
            is_verified=True,
            is_superuser=True

        )
        async_session.add(user)
        await async_session.commit()
        return user


@pytest.fixture
async def create_employee(session):
    async with session as async_session:
        user = User(
            email="alex@gmail.com",
            hashed_password=context.hash("12345"),
            name="Alex",
            salary=2500,
            role=UserRoleEnum.EMPLOYEE,
            is_verified=True
        )
        async_session.add(user)
        await async_session.commit()
        return user


@pytest.fixture
async def create_user(session):
    async with session as async_session:
        user = User(
            email="ivan@gmail.com",
            hashed_password=context.hash("12345"),
            name="Ivan"
        )
        async_session.add(user)
        await async_session.commit()
        return user
