from datetime import datetime

from fastapi import Depends, HTTPException

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.request.model import Request, AssigneeEnum, StatusEnum
from src.api.request.schema import RequestCreate
from src.api.user.model import User, UserRoleEnum
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

        await session.commit()

        return request

    else:
        raise HTTPException(status_code=403, detail="Can't redirect")


async def delete_one_request(request_id: int,
                             current_user: User,
                             session: AsyncSession):
    request = await get_request_id(request_id, session)

    if not request:
        raise HTTPException(status_code=404, detail=f"Request with ID {request_id} not found.")

    elif request.status == StatusEnum.CLOSED:
        raise HTTPException(status_code=403, detail="can't delete a closed request")

    elif request.user_id != current_user.id and current_user.role != UserRoleEnum.ADMIN.value:
        raise HTTPException(status_code=403, detail="Forbidden")

    else:
        await session.delete(request)
        await session.commit()

        return {"message": f"Request with ID {request_id} was successfully deleted."}







