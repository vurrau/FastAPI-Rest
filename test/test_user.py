from httpx import AsyncClient


async def test_get_staff_user(ac: AsyncClient, create_admin):
    response = await ac.get("/user/staff")
    assert response.status_code == 200
    assert "application/json" in response.headers["content-type"]

    staff_members = response.json()

    assert len(staff_members) > 0

    for member in staff_members:

        assert "name" in member
        assert "role" in member

    expected_data = {
        "name": "Pavel",
        "role": "ADMIN",
    }
    assert expected_data in staff_members

