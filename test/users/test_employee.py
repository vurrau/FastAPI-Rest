from httpx import AsyncClient

from test.users.fixtures.user_fixtures import create_user, create_employee, create_manager
from test.users.fixtures.token_fixtures import auth_token_employee, auth_token_user, auth_token_manager


async def test_full_info_employee(ac: AsyncClient, auth_token_manager, create_employee):
    employee = create_employee
    response = await ac.get("/employee/info/full", headers=auth_token_manager)

    assert response.status_code == 200
    assert "application/json" in response.headers["content-type"]

    employee_members = response.json()

    assert len(employee_members) > 0

    expected_data = {
        "email": employee.email,
        "id": employee.id,
        "name": employee.name,
        "role": employee.role.value,
        "salary": employee.salary,
    }
    assert expected_data in employee_members


async def test_basic_info_employee(ac: AsyncClient, auth_token_employee, create_employee):
    employee = create_employee
    response = await ac.get("/employee/info/basic", headers=auth_token_employee)

    assert response.status_code == 200
    assert "application/json" in response.headers["content-type"]

    employee_members = response.json()

    assert len(employee_members) > 0

    expected_data = {
        "name": employee.name,
        "email": employee.email,
        "id": employee.id,
        "role": employee.role.value
    }
    assert expected_data in employee_members


async def test_info_employee(ac: AsyncClient, create_manager):
    manager = create_manager
    response = await ac.get("/employee/info")

    assert response.status_code == 200
    assert "application/json" in response.headers["content-type"]

    staff_members = response.json()

    assert len(staff_members) > 0

    expected_data = {
        "name": manager.name,
        "email": manager.email,
    }
    assert expected_data in staff_members


