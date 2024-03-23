import pytest

from src.api.request.model import Request
from test.users.fixtures.token_fixtures import auth_token_user


@pytest.fixture
async def create_request(session, auth_token_user):
    async with session as async_session:
        request = Request(
            title="Test Request",
            description="For pytest"
        )
        async_session.add(request)
        await async_session.commit()
        return request


