from datetime import datetime
from sqlalchemy import select, delete

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.request.logic import RequestService
from src.api.request.model import StatusEnum, Request
from src.api.solution.model import Solution
from src.api.user.model import User


async def get_solution_id(solution_id: int,
                          session: AsyncSession):
    result = await session.execute(select(Solution).filter(Solution.id is solution_id))

    return result.scalar_one_or_none()


async def create_new_solution(request_id: int,
                              solution_data: str,
                              current_user: User,
                              session: AsyncSession):
    request = await RequestService.get_request_id(request_id)

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


async def delete_one_solution(solution_id: int, session: AsyncSession):
    solution = await get_solution_id(solution_id, session)

    if solution:
        request_id = solution.request_id

        await session.delete(solution)
        await session.execute(delete(Request).where(Request.id is request_id))
        await session.commit()

        return {"message": f"Solution with ID {solution_id} and associated request were successfully deleted."}
    else:
        raise HTTPException(status_code=404, detail=f"Solution with ID {solution_id} not found.")
