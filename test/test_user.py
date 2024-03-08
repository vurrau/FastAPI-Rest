from fastapi import Depends
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.models import User
from conftest import override_get_async_session


async def test_get_staff_user(ac: AsyncClient, create_admin):
    response = await ac.get("/user/staff")
    assert response.status_code == 200
    staff_members = response.json()
    assert any(member["name"] == "Pavel" and member["role"] == "ADMIN" for member in staff_members)

