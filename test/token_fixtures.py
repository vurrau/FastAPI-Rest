import pytest

from httpx import AsyncClient


@pytest.fixture
async def auth_token_staff(ac: AsyncClient, create_staff):
    response = await ac.post("/auth/login", data={"username": "alex@gmail.com", "password": "12345"})
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
