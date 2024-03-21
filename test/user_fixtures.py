import pytest
from passlib.context import CryptContext

from src.api.user.model import UserRoleEnum, User

context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@pytest.fixture
async def create_admin(session):
    async with session as async_session:
        user = User(
            email="pavel@gmail.com",
            hashed_password=context.hash("12345"),
            name="Pavel",
            role=UserRoleEnum.ADMIN,
            is_verified=True,
            is_superuser=True
        )
        async_session.add(user)
        await async_session.commit()
        return user


@pytest.fixture
async def create_staff(session):
    async with session as async_session:
        user = User(
            email="alex@gmail.com",
            hashed_password=context.hash("12345"),
            name="Alex",
            salary=2500,
            role=UserRoleEnum.STAFF,
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
