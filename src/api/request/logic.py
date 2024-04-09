from datetime import datetime

from fastapi import HTTPException

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.request.model import Request, AssigneeEnum, StatusEnum
from src.api.request.schema import RequestCreate
from src.api.user.model import User, UserRoleEnum
from src.core.db.base import get_async_session


class RequestService:
    @staticmethod
    async def get_request_id(request_id: int, session: AsyncSession):
        result = await session.execute(select(Request).filter(Request.id == request_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def create_new_request(current_user: User, request_data: RequestCreate, session: AsyncSession):
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

    @staticmethod
    async def get_all_request(current_user: User, session: AsyncSession):
        """
        Depending on the role, we get a list of queries.
        """
        query = select(Request).filter(Request.assignee == current_user.role.name)

        result = await session.execute(query)
        return result.scalars().all()

    @staticmethod
    async def redirection(request_id: int, current_user: User, session: AsyncSession):
        """
        If an employee cannot provide a solution to a request,
        he can forward it to the manager.
        """
        request = await RequestService.get_request_id(request_id, session)

        if current_user.role.value == AssigneeEnum.EMPLOYEE.value:
            request.assignee = AssigneeEnum.MANAGER
            request.status = StatusEnum.PROCESSING

            session.add(request)
            await session.commit()
            return request

        else:
            raise HTTPException(status_code=403, detail="Can't redirect")

    @staticmethod
    async def delete_one_request(request_id: int, current_user: User, session: AsyncSession):
        """
        a user can only delete his request,
        until it is resolved.

        In the same way, the manager can also delete.
        """
        request = await RequestService.get_request_id(request_id, session)

        if not request:
            raise HTTPException(status_code=404, detail=f"Request with ID {request_id} not found.")

        elif request.status == StatusEnum.CLOSED:
            raise HTTPException(status_code=403, detail="can't delete a closed request")

        elif request.user_id != current_user.id and current_user.role != UserRoleEnum.MANAGER:
            raise HTTPException(status_code=403, detail="Forbidden")

        try:
            await session.delete(request)
            await session.commit()
            return {"message": f"Request with ID {request_id} was successfully deleted."}

        except Exception as e:
            await session.rollback()
            raise HTTPException(status_code=500, detail=f"Failed to delete request: {str(e)}")
