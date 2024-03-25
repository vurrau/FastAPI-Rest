from typing import Annotated

from fastapi import APIRouter, Depends, BackgroundTasks

from src.api.request.logic import RequestService
from src.api.request.schema import RequestCreate, RequestInfo
from src.api.user.model import User

from src.services.manager import current_active_user, current_employee

from src.tasks.tasks import send_create_request

request = APIRouter(
    prefix="/request",
    tags=["request"]
)


@request.post("/create", response_model=RequestInfo)
async def create_request(data: Annotated[RequestCreate, Depends()],
                         background_tasks: BackgroundTasks,
                         current_user: User = Depends(current_active_user)
                         ):
    result = await RequestService.create_new_request(current_user, data)

    # await send_create_request(background_tasks, data)

    return result


@request.get("/", response_model=list[RequestInfo])
async def get_request(current_user: User = Depends(current_employee)):
    result = await RequestService.get_all_request(current_user)

    return result


@request.patch("/redirection", response_model=RequestInfo)
async def redirection_request(request_id: int, current_user: User = Depends(current_employee)):
    result = await RequestService.redirection(request_id, current_user)

    return result


@request.delete("/delete")
async def delete_request(request_id: int, current_user: User = Depends(current_active_user)):
    result = await RequestService.delete_one_request(request_id, current_user)

    return result


