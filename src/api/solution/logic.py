from datetime import datetime
from sqlalchemy import select, delete

from fastapi import HTTPException

from src.api.request.logic import RequestService
from src.api.request.model import StatusEnum, Request
from src.api.solution.model import Solution
from src.api.user.model import User
from src.core.db.base import async_session_maker


class SolutionService:
    @staticmethod
    async def get_solution_id(solution_id: int):
        async with async_session_maker() as session:
            result = await session.execute(select(Solution).filter(Solution.id == solution_id))
            return result.scalar_one_or_none()

    @staticmethod
    async def create_new_solution(request_id: int,
                                  solution_data: str,
                                  current_user: User):
        async with async_session_maker() as session:
            request = await RequestService.get_request_id(request_id)

            if request:
                new_solution = Solution(
                    description=solution_data,
                    response_at=datetime.now(),
                    request_id=request_id,
                    username=current_user.name
                    )

                request.status = StatusEnum.CLOSED

                session.add(new_solution)
                session.add(request)

                await session.commit()
                await session.refresh(new_solution)

                return new_solution

            else:
                raise HTTPException(status_code=404, detail="Request not found")

    @staticmethod
    async def delete_one_solution(solution_id: int):
        async with async_session_maker() as session:
            solution = await SolutionService.get_solution_id(solution_id)

            if solution:
                request_id = solution.request_id

                await session.delete(solution)
                await session.execute(delete(Request).where(Request.id == request_id))
                await session.commit()

                return {"message": f"Solution with ID {solution_id} and associated request were successfully deleted."}
            else:
                raise HTTPException(status_code=404, detail=f"Solution with ID {solution_id} not found.")
