from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.request.logic import create_new_request
from src.api.request.schema import RequestCreate
from src.api.user.model import User
from src.core.db.base import get_async_session
from src.services.manager import fastapi_users

request = APIRouter(
    prefix="/request",
    tags=["request"]
)

current_active_user = fastapi_users.current_user(active=True)


@request.post("/create")
async def create_request(request_data: RequestCreate,
                         session: AsyncSession = Depends(get_async_session),
                         current_user: User = Depends(current_active_user)):
    create = await create_new_request(current_user, request_data, session)

    return create
