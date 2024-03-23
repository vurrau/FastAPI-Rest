from httpx import AsyncClient

from fixtures.token_fixtures import auth_token_staff
from test.users.fixtures.user_fixtures import create_user, create_staff


async def test_get_info_employee(ac: AsyncClient, auth_token_staff, create_staff):
    response = await ac.get("/staff/employee", headers=auth_token_staff)

    assert response.status_code == 200
    assert "application/json" in response.headers["content-type"]

    staff = create_staff

    staff_members = response.json()

    assert len(staff_members) > 0

    expected_data = {
        "name": staff.name,
        "email": staff.email,
        "id": staff.id,
        "role": staff.role.value
    }
    assert expected_data in staff_members


async def test_get_info_user(ac: AsyncClient, create_user, auth_token_staff):
    response = await ac.get("/staff/user", headers=auth_token_staff)

    assert response.status_code == 200
    assert "application/json" in response.headers["content-type"]

    user = create_user

    staff_members = response.json()

    assert len(staff_members) > 0

    expected_data = {
        "id": user.id,
        "name": user.name,
        "email": user.email
    }
    assert expected_data in staff_members


