from httpx import AsyncClient

from src.api.request.model import StatusEnum, AssigneeEnum
from test.users.fixtures.token_fixtures import auth_token_user
from test.users.fixtures.user_fixtures import create_user


async def test_create_request(ac: AsyncClient, auth_token_user, create_user):
    response = await ac.post("/request/create",
                             headers=auth_token_user,
                             json={"title": "test", "description": "create request test"}
                             )
    assert response.status_code == 200
    assert "application/json" in response.headers["content-type"]

    request_data = response.json()

    assert request_data["title"] == "test"
    assert request_data["description"] == "create request test"
    assert request_data["assignee"] == AssigneeEnum.STAFF.value
    assert request_data["status"] == StatusEnum.OPEN.value
    assert request_data["user_id"] == create_user.id

    # stored_request = await session.execute(
    #     session.query(Request).filter(Request.id == request_data["id"])
    # )
    # assert stored_request is not None
