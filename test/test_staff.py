from httpx import AsyncClient


async def test_get_staff(ac: AsyncClient, auth_token_staff):
    response = await ac.get("/staff/", headers=auth_token_staff)

    assert response.status_code == 200
    assert "application/json" in response.headers["content-type"]

    staff_members = response.json()

    assert len(staff_members) > 0

    for member in staff_members:

        assert "name" in member
        assert "email" in member

    expected_data = {
        "name": "Serg",
        "email": "serg@gmail.com",
    }
    assert expected_data in staff_members


async def test_get_user_name(ac: AsyncClient, create_user, auth_token_staff):
    response = await ac.get("/staff/user", headers=auth_token_staff)

    assert response.status_code == 200

    assert response.json() == ["Ivan"]
