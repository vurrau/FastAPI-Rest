import asyncio
from typing import AsyncGenerator

import pytest

from httpx import AsyncClient, ASGITransport
from sqlalchemy import select, delete
from sqlalchemy.pool import NullPool

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from src.api.models import UserRoleEnum, User
from src.main import app
from src.db.base import get_async_session, Base

from src.config import DB_USER_TEST, DB_HOST_TEST, DB_PASS_TEST, DB_PORT_TEST, DB_NAME_TEST

DATABASE_URL_TEST = f"postgresql+asyncpg://{DB_USER_TEST}:{DB_PASS_TEST}@{DB_HOST_TEST}:{DB_PORT_TEST}/{DB_NAME_TEST}"

engine_test = create_async_engine(DATABASE_URL_TEST, poolclass=NullPool)
async_session_maker = async_sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


app.dependency_overrides[get_async_session] = override_get_async_session


@pytest.fixture(autouse=True, scope='session')
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope='session')
def custom_event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session')
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test', follow_redirects=True) as ac:
        yield ac


@pytest.fixture
async def session():
    session = async_session_maker()
    try:
        yield session
    finally:
        await session.close()


@pytest.fixture(autouse=True)
async def cleanup_all_data(session):
    yield
    async with session.begin():
        await session.execute(delete(User))


@pytest.fixture
async def create_admin(ac: AsyncClient, session):
    response = await ac.post("/auth/register", json={
        "email": "pavel@gmail.com",
        "password": "12345",
        "name": "Pavel"
    })
    assert response.status_code == 201

    async with session as async_session:
        result = await async_session.execute(select(User).where(User.email == "pavel@gmail.com"))
        user = result.scalars().first()

        assert user is not None

        user.role = UserRoleEnum.ADMIN
        user.is_verified = True
        user.is_superuser = True

        await async_session.commit()

    return user


@pytest.fixture
async def create_staff(ac: AsyncClient, session):
    response = await ac.post("/auth/register", json={
        "email": "serg@gmail.com",
        "password": "12345",
        "name": "Serg"
    })
    assert response.status_code == 201

    async with session as async_session:
        result = await async_session.execute(select(User).where(User.email == "serg@gmail.com"))
        user = result.scalars().first()

        assert user is not None

        user.salary = 2500
        user.role = UserRoleEnum.STAFF
        user.is_verified = True

        await async_session.commit()

    return user


@pytest.fixture
async def create_user(ac: AsyncClient, session):
    response = await ac.post("/auth/register", json={
        "email": "ivan@gmail.com",
        "password": "12345",
        "name": "Ivan"
    })
    assert response.status_code == 201

    return response


@pytest.fixture
async def auth_token_staff(ac: AsyncClient, create_staff):
    response = await ac.post("/auth/login", data={"username": "serg@gmail.com", "password": "12345"})
    assert response.status_code == 204

    token_cookie = response.cookies.get("fastapiusersauth")
    assert token_cookie is not None

    token = token_cookie
    headers = {"Cookie": f"fastapiusersauth={token}"}
    return headers


@pytest.fixture
async def auth_token_admin(ac: AsyncClient, create_admin):
    response = await ac.post("/auth/login", data={"username": "pavel@gmail.com", "password": "12345"})
    assert response.status_code == 204

    token_cookie = response.cookies.get("fastapiusersauth")
    assert token_cookie is not None

    token = token_cookie
    headers = {"Cookie": f"fastapiusersauth={token}"}
    return headers



