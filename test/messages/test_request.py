from datetime import datetime

from httpx import AsyncClient

from src.api.request.model import StatusEnum, AssigneeEnum
from src.api.user.model import UserRoleEnum
from test.users.fixtures.token_fixtures import auth_token_user, auth_token_employee, auth_token_manager
from test.users.fixtures.user_fixtures import create_user, create_employee, create_manager
from test.messages.fixtures.request_fixtures import create_request


async def test_create_request(ac: AsyncClient, auth_token_user, create_user):
    user = create_user
    response = await ac.post("/request/create",
                             headers=auth_token_user,
                             params={"title": "test", "description": "create request test"}
                             )
    assert response.status_code == 200
    assert "application/json" in response.headers["content-type"]

    request_data = response.json()

    assert request_data["title"] == "test"
    assert request_data["description"] == "create request test"
    assert request_data["assignee"] == AssigneeEnum.EMPLOYEE.value
    assert request_data["status"] == StatusEnum.OPEN.value
    assert request_data["user_id"] == user.id


async def test_get_request(ac: AsyncClient, auth_token_employee, create_request):
    request = create_request
    response = await ac.get("/request/info", headers=auth_token_employee)

    assert response.status_code == 200
    assert "application/json" in response.headers["content-type"]

    request_members = response.json()

    assert len(request_members) > 0

    expected_data = {
        "id": request.id,
        "title": request.title,
        "description": request.description,
        "status": request.status.value,
        "assignee": request.assignee.value,
        "user_id": request.user_id,
        "created_at": request.created_at.isoformat()
    }
    assert expected_data in request_members


async def test_redirection_request(ac: AsyncClient, auth_token_employee, create_request):
    request = create_request
    response = await ac.patch("/request/redirection",
                            headers=auth_token_employee,
                            params={"request_id": request.id}
                            )

    assert response.status_code == 200
    assert "application/json" in response.headers["content-type"]

    request_data = response.json()

    assert request_data["id"] == request.id
    assert request_data["title"] == request.title
    assert request_data["description"] == request.description
    assert request_data["status"] == StatusEnum.PROCESSING.value
    assert request_data["assignee"] == UserRoleEnum.MANAGER.value
    assert request_data["user_id"] == request.user_id
    assert request_data["created_at"] == request.created_at.isoformat()


async def test_delete_request(ac: AsyncClient, auth_token_manager, auth_token_employee, create_request):
    request = create_request
    response = await ac.delete("/request/delete",
                               headers=auth_token_manager,
                               params={"request_id": request.id})

    assert response.status_code == 200
    assert "application/json" in response.headers["content-type"]

    assert response.json() == {"message": f"Request with ID {request.id} was successfully deleted."}

    response_not_found = await ac.delete("/request/delete",
                               headers=auth_token_manager,
                               params={"request_id": request.id})

    assert response_not_found.status_code == 404
    assert response_not_found.json() == {"detail": f"Request with ID {request.id} not found."}

