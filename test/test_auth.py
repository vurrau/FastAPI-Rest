from httpx import AsyncClient


async def test_register(ac: AsyncClient):
    response = await ac.post("/auth/register", json={
        "email": "123@gmail.com",
        "password": "12345",
        "name": "Pavel"
    })

    assert response.status_code == 201




