from httpx import AsyncClient

from user_fixtures import create_admin


async def test_get_name_employee(ac: AsyncClient, create_admin):
    response = await ac.get("/user/staff")

    assert response.status_code == 200
    assert "application/json" in response.headers["content-type"]

    staff_members = response.json()

    assert len(staff_members) > 0

    expected_data = {
        "name": create_admin.name,
        "email": create_admin.email,
    }
    assert expected_data in staff_members

