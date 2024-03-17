from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.request.logic import create_new_request, redirection, get_all_request, delete_one_request

from src.api.request.schema import RequestCreate
from src.api.user.model import User
from src.core.db.base import get_async_session
from src.services.manager import fastapi_users

request = APIRouter(
    prefix="/request",
    tags=["request"]
)

current_active_user = fastapi_users.current_user(active=True)
current_employee = fastapi_users.current_user(active=True, verified=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)


@request.post("/create")
async def create_request(request_data: RequestCreate,
                         session: AsyncSession = Depends(get_async_session),
                         current_user: User = Depends(current_active_user)
                         ):
    create = await create_new_request(current_user, request_data, session)

    return create


@request.get("/")
async def get_request(
        session: AsyncSession = Depends(get_async_session),
        current_user: User = Depends(current_employee)
):
    requests = await get_all_request(current_user, session)

    return requests


@request.patch("/redirection")
async def redirection_request(request_id: int,
                              current_user: User = Depends(current_employee),
                              session: AsyncSession = Depends(get_async_session)
                              ):
    modified_request = await redirection(request_id, current_user, session)

    return modified_request


@request.delete("/")
async def delete_request(request_id: int,
                         current_user: User = Depends(current_active_user),
                         session: AsyncSession = Depends(get_async_session)):
    result = await delete_one_request(request_id, current_user, session)

    return result


