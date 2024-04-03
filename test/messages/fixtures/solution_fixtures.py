from datetime import datetime

import pytest

from src.api.solution.model import Solution
from test.users.fixtures.user_fixtures import create_employee, create_manager
from test.messages.fixtures.request_fixtures import create_request


@pytest.fixture
async def create_solution(session, create_request, create_employee):
    request = create_request
    employee = create_employee
    async with session as async_session:
        solution = Solution(
            description="For pytest",
            username=employee.name,
            request_id=request.id,
            response_at=datetime.now()
        )
        async_session.add(solution)
        await async_session.commit()
        return solution

