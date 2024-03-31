from httpx import AsyncClient

from test.users.fixtures.user_fixtures import create_user, create_employee, create_manager
from test.users.fixtures.token_fixtures import auth_token_employee, auth_token_user, auth_token_manager


async def test_get_info_user(ac: AsyncClient, create_user, auth_token_employee):
    response = await ac.get("/user/info/basic", headers=auth_token_employee)

    assert response.status_code == 200
    assert "application/json" in response.headers["content-type"]

    user = create_user

    employee_members = response.json()

    assert len(employee_members) > 0

    expected_data = {
        "id": user.id,
        "name": user.name,
        "email": user.email
    }
    assert expected_data in employee_members


async def test_get_info_user(ac: AsyncClient, create_user):
    response = await ac.get("/user/info")

    assert response.status_code == 200
    assert "application/json" in response.headers["content-type"]

    user_members = response.json()

    user = create_user

    assert len(user_members) > 0

    expected_data = {
        "name": user.name
    }
    assert expected_data in user_members

