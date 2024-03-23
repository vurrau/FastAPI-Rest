from fastapi import APIRouter, Depends, BackgroundTasks

from sqlalchemy.ext.asyncio import AsyncSession

from src.api.request.logic import create_new_request, redirection, get_all_request, delete_one_request
from src.api.request.schema import RequestCreate, RequestRead
from src.api.user.model import User

from src.core.db.base import get_async_session
from src.services.manager import current_active_user, current_employee

from src.tasks.tasks import send_create_request

request = APIRouter(
    prefix="/request",
    tags=["request"]
)


@request.post("/create", response_model=RequestCreate)
async def create_request(request_data: RequestCreate,
                         background_tasks: BackgroundTasks,
                         session: AsyncSession = Depends(get_async_session),
                         current_user: User = Depends(current_active_user)
                         ):
    result = await create_new_request(current_user, request_data, session)

    await send_create_request(background_tasks, session, request_data)

    return result


@request.get("/", response_model=list[RequestRead])
async def get_request(
        session: AsyncSession = Depends(get_async_session),
        current_user: User = Depends(current_employee)
):
    result = await get_all_request(current_user, session)

    return result


@request.patch("/redirection", response_model=RequestRead)
async def redirection_request(request_id: int,
                              current_user: User = Depends(current_employee),
                              session: AsyncSession = Depends(get_async_session)
                              ):
    result = await redirection(request_id, current_user, session)

    return result


@request.delete("/delete")
async def delete_request(request_id: int,
                         current_user: User = Depends(current_active_user),
                         session: AsyncSession = Depends(get_async_session)):
    result = await delete_one_request(request_id, current_user, session)

    return result


