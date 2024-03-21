# from httpx import AsyncClient
#
#
# async def test_get_staff_admin(ac: AsyncClient, auth_token_admin, create_staff):
#     response = await ac.get("/admin/staff", headers=auth_token_admin)
#
#     assert response.status_code == 200
#     assert "application/json" in response.headers["content-type"]
#
#     staff_members = response.json()
#
#     assert len(staff_members) > 0
#
#     expected_data = {
#         "email": create_staff.email,
#         "id": create_staff.id,
#         "name": create_staff.name,
#         "role": "STAFF",
#         "salary": create_staff.salary,
#     }
#     assert expected_data in staff_members
#
#
# async def test_update_role(ac: AsyncClient, auth_token_admin, create_user):
#     response = await ac.put("/admin/role",
#                             headers=auth_token_admin,
#                             params={"user_id": create_user.id, "new_role": "STAFF"}
#                             )
#
#     assert response.status_code == 200
#     assert "application/json" in response.headers["content-type"]
#
#     user = create_user
#
#     user_data = response.json()
#
#     assert user_data["id"] == user.id
#     assert user_data["email"] == user.email
#     assert user_data["name"] == user.name
#     assert user_data["role"] == "STAFF"
#
#
# async def test_update_staff_salary(ac: AsyncClient, auth_token_admin, create_staff):
#     response = await ac.put("/admin/salary",
#                             headers=auth_token_admin,
#                             params={"user_id": create_staff.id, "new_salary": 2222}
#                             )
#
#     assert response.status_code == 200
#     assert "application/json" in response.headers["content-type"]
#
#     staff_members = response.json()
#
#     assert len(staff_members) > 0
#
#     expected_data = {
#         "id": create_staff.id,
#         "email": create_staff.email,
#         "name": create_staff.name,
#         "role": "STAFF",
#         "salary": 2222,
#
#     }
#     assert expected_data in staff_members
