import asyncio
from typing import AsyncGenerator

import pytest

from httpx import AsyncClient, ASGITransport
from sqlalchemy.pool import NullPool

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from src.api.models import User
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
async def create_admin(session):
    admin_data = {
        "name": "Pavel",
        "email": "pavel@gmail.com",
        "role": "ADMIN",
        "hashed_password": "12345",
        "is_superuser": True
    }
    admin = User(**admin_data)
    session.add(admin)
    await session.commit()
    return admin


@pytest.fixture
async def session():
    session = async_session_maker()
    try:
        yield session
    finally:
        await session.close()
