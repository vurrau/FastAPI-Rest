from httpx import AsyncClient
from token_fixtures import auth_token_staff
from user_fixtures import create_user, create_staff


async def test_get_info_employee(ac: AsyncClient, auth_token_staff, create_staff):
    response = await ac.get("/staff/", headers=auth_token_staff)

    assert response.status_code == 200
    assert "application/json" in response.headers["content-type"]

    staff_members = response.json()

    assert len(staff_members) > 0

    expected_data = {
        "name": create_staff.name,
        "email": create_staff.email,
        "id": create_staff.id,
        "role": create_staff.role.value
    }
    assert expected_data in staff_members


async def test_get_user_name(ac: AsyncClient, create_user, auth_token_staff):
    response = await ac.get("/staff/user", headers=auth_token_staff)

    assert response.status_code == 200
    assert "application/json" in response.headers["content-type"]

    staff_members = response.json()

    assert len(staff_members) > 0

    expected_data = {
        "id": create_user.id,
        "name": create_user.name,
        "email": create_user.email
    }
    assert expected_data in staff_members


