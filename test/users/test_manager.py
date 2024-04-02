from httpx import AsyncClient

from src.api.user.model import UserRoleEnum
from test.users.fixtures.user_fixtures import create_user, create_employee, create_manager
from test.users.fixtures.token_fixtures import auth_token_employee, auth_token_user, auth_token_manager


async def test_update_role(ac: AsyncClient, auth_token_manager, create_user):
    response = await ac.patch("/manager/role",
                            headers=auth_token_manager,
                            params={"user_id": create_user.id, "new_role": "EMPLOYEE"}
                            )

    assert response.status_code == 200
    assert "application/json" in response.headers["content-type"]

    user = create_user

    user_data = response.json()

    assert user_data["id"] == user.id
    assert user_data["email"] == user.email
    assert user_data["name"] == user.name
    assert user_data["role"] == UserRoleEnum.EMPLOYEE.value


async def test_update_salary(ac: AsyncClient, auth_token_manager, create_employee):
    response = await ac.patch("/manager/salary",
                            headers=auth_token_manager,
                            params={"user_id": create_employee.id, "new_salary": 2222}
                            )

    assert response.status_code == 200
    assert "application/json" in response.headers["content-type"]

    employee = create_employee

    employee_members = response.json()

    assert len(employee_members) > 0

    assert employee_members["id"] == employee.id
    assert employee_members["email"] == employee.email
    assert employee_members["name"] == employee.name
    assert employee_members["role"] == employee.role.value
    assert employee_members["salary"] == 2222

