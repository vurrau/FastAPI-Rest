from datetime import datetime

from httpx import AsyncClient

from test.users.fixtures.token_fixtures import auth_token_employee, auth_token_manager, auth_token_user
from test.users.fixtures.user_fixtures import create_employee, create_manager, create_user
from test.messages.fixtures.request_fixtures import create_request
from test.messages.fixtures.solution_fixtures import create_solution


async def test_create_solution(ac: AsyncClient, auth_token_employee, create_employee, create_request):
    request = create_request
    employee = create_employee
    response = await ac.post("/solution/create",
                             headers=auth_token_employee,
                             params={"request_id": request.id, "solution_data": "answer test"}
                             )
    assert response.status_code == 200
    assert "application/json" in response.headers["content-type"]

    request_data = response.json()

    assert request_data["description"] == "answer test"
    assert request_data["username"] == employee.name
    assert request_data["request_id"] == request.id


async def test_delete_solution(ac: AsyncClient, auth_token_manager, create_request, create_solution):
    solution = create_solution
    response = await ac.delete("/solution/delete",
                               headers=auth_token_manager,
                               params={"solution_id": solution.id})
    assert response.status_code == 200
    assert "application/json" in response.headers["content-type"]

    assert (response.json() ==
            {"message": f"Solution with ID {solution.id} and associated request were successfully deleted."})

    response_not_found = await ac.delete("/solution/delete",
                                         headers=auth_token_manager,
                                         params={"solution_id": solution.id})

    assert response_not_found.status_code == 404
    assert response_not_found.json() == {"detail": f"Solution with ID {solution.id} not found."}
