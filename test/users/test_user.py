from httpx import AsyncClient

from test.users.fixtures.user_fixtures import create_user, create_staff, create_admin, create_manager


async def test_get_name_employee(ac: AsyncClient, create_admin):
    response = await ac.get("/user/employee")

    assert response.status_code == 200
    assert "application/json" in response.headers["content-type"]

    staff_members = response.json()

    admin = create_admin

    assert len(staff_members) > 0

    expected_data = {
        "name": admin.name,
        "email": admin.email,
    }
    assert expected_data in staff_members


async def test_get_info_user(ac: AsyncClient, create_user):
    response = await ac.get("/user")

    assert response.status_code == 200
    assert "application/json" in response.headers["content-type"]

    staff_members = response.json()

    user = create_user

    assert len(staff_members) > 0

    expected_data = {
        "name": user.name
    }
    assert expected_data in staff_members

