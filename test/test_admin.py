from httpx import AsyncClient


async def test_get_staff_admin(ac: AsyncClient, auth_token_admin, create_staff):
    response = await ac.get("/admin/staff", headers=auth_token_admin)

    assert response.status_code == 200
    assert "application/json" in response.headers["content-type"]

    staff_members = response.json()

    assert len(staff_members) > 0

    for member in staff_members:
        assert "email" in member
        assert "salary" in member
        assert "name" in member
        assert "id" in member
        assert "role" in member

    expected_data = {
        "email": "serg@gmail.com",
        "salary": 2500,
        "name": "Serg",
        "id": 2,
        "role": "STAFF",
    }
    assert expected_data in staff_members
