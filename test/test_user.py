from httpx import AsyncClient


async def test_get_staff_user(ac: AsyncClient):
    response = await ac.post("/user/staff", params={
        "username": "Pavel"
    })
