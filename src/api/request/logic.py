from datetime import datetime

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.request.model import Request, StatusEnum
from src.api.request.schema import RequestCreate
from src.api.user.model import User
from src.core.db.base import get_async_session


async def create_new_request(current_user: User,
                             request_data: RequestCreate,
                             session: AsyncSession = Depends(get_async_session)):
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
        session: AsyncSession = Depends(get_async_session)):

    query = select(Request).filter(Request.assignee == current_user.role.name)

    result = await session.execute(query)

    return result.mappings().all()
