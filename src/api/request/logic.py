from datetime import datetime

from fastapi import Depends, HTTPException

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.request.model import Request, AssigneeEnum, StatusEnum
from src.api.request.schema import RequestCreate
from src.api.user.model import User
from src.core.db.base import get_async_session


async def get_request_id(request_id: int,
                         session: AsyncSession):

    result = await session.execute(select(Request).filter(Request.id == request_id))

    return result.scalar_one_or_none()


async def create_new_request(current_user: User,
                             request_data: RequestCreate,
                             session: AsyncSession):
    new_request = Request(
        title=request_data.title,
        description=request_data.description,
        created_at=datetime.now(),
        user_id=current_user.id
    )

    session.add(new_request)

    await session.commit()
    await session.refresh(new_request)

    return new_request


async def get_all_request(
        current_user: User,
        session: AsyncSession):

    query = select(Request).filter(Request.assignee == current_user.role.name)

    result = await session.execute(query)

    return result.scalars().all()


async def redirection(
        request_id: int,
        current_user: User,
        session: AsyncSession = Depends(get_async_session)):
    request = await get_request_id(request_id, session)

    if current_user.role.value == AssigneeEnum.STAFF.value:
        request.assignee = AssigneeEnum.MANAGER
        request.status = StatusEnum.PROCESSING

        return request

    else:
        raise HTTPException(status_code=409, detail="Can't redirect")


