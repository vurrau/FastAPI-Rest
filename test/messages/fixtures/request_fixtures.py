from datetime import datetime

import pytest

from src.api.request.model import Request
from test.users.fixtures.token_fixtures import auth_token_user, auth_token_employee, auth_token_manager
from test.users.fixtures.user_fixtures import create_user, create_employee, create_manager


@pytest.fixture
async def create_request(session, auth_token_user, create_user):
    user = create_user
    async with session as async_session:
        request = Request(
            title="Test Request",
            description="For pytest",
            user_id=user.id,
            created_at=datetime.now()
        )
        async_session.add(request)
        await async_session.commit()
        return request





