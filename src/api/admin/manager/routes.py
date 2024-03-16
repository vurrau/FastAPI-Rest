from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.request.logic import get_all_request
from src.services.manager import fastapi_users
from src.api.user.model import User
from src.core.db.base import get_async_session

manager = APIRouter(
    prefix="/manager",
    tags=["manager"]
)

current_manager = fastapi_users.current_user(active=True, verified=True)


@manager.get("/request")
async def get_request(
        session: AsyncSession = Depends(get_async_session),
        current_user: User = Depends(current_manager)):

    requests = await get_all_request(current_user, session)

    return requests
