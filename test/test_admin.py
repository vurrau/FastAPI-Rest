from httpx import AsyncClient

from src.api.user.model import UserRoleEnum
from token_fixtures import auth_token_admin, auth_token_staff, auth_token_user, auth_token_manager
from user_fixtures import create_user, create_staff, create_admin, create_manager


async def test_get_full_info_employee(ac: AsyncClient, auth_token_admin, create_staff):
    response = await ac.get("/admin/employee", headers=auth_token_admin)

    assert response.status_code == 200
    assert "application/json" in response.headers["content-type"]

    staff = create_staff

    staff_members = response.json()

    assert len(staff_members) > 0

    expected_data = {
        "email": staff.email,
        "id": staff.id,
        "name": staff.name,
        "role": staff.role.value,
        "salary": staff.salary,
    }
    assert expected_data in staff_members


async def test_update_role(ac: AsyncClient, auth_token_admin, create_user):
    response = await ac.patch("/admin/role",
                            headers=auth_token_admin,
                            params={"user_id": create_user.id, "new_role": "STAFF"}
                            )

    assert response.status_code == 200
    assert "application/json" in response.headers["content-type"]

    user = create_user

    user_data = response.json()

    assert user_data["id"] == user.id
    assert user_data["email"] == user.email
    assert user_data["name"] == user.name
    assert user_data["role"] == UserRoleEnum.STAFF.value


async def test_update_salary(ac: AsyncClient, auth_token_admin, create_staff):
    response = await ac.patch("/admin/salary",
                            headers=auth_token_admin,
                            params={"user_id": create_staff.id, "new_salary": 2222}
                            )

    assert response.status_code == 200
    assert "application/json" in response.headers["content-type"]

    staff = create_staff

    staff_members = response.json()

    assert len(staff_members) > 0

    assert staff_members["id"] == staff.id
    assert staff_members["email"] == staff.email
    assert staff_members["name"] == staff.name
    assert staff_members["role"] == staff.role.value
    assert staff_members["salary"] == 2222

