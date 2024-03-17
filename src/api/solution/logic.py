from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.request.logic import get_request_id
from src.api.request.model import Request, StatusEnum
from src.api.solution.model import Solution
from src.api.user.model import User


async def create_new_solution(request_id: int,
                              solution_data: str,
                              current_user: User,
                              session: AsyncSession):
    request = await get_request_id(request_id, session)

    if request:
        new_solution = Solution(
            description=solution_data,
            response_at=datetime.now(),
            request_id=request_id,
            username=current_user.name
            )

        session.add(new_solution)

        request.status = StatusEnum.CLOSED

        await session.commit()
        await session.refresh(new_solution)

        return request, new_solution

    else:
        raise HTTPException(status_code=404, detail="Request not found")
