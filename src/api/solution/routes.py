from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.solution.logic import create_new_solution
from src.services.manager import fastapi_users
from src.api.user.model import User
from src.core.db.base import get_async_session

solution = APIRouter(
    prefix="/solution",
    tags=["solution"]
)

current_employee = fastapi_users.current_user(active=True, verified=True)


@solution.post("/create")
async def create_solution(request_id: int,
                          solution_data: str,
                          current_user: User = Depends(current_employee),
                          session: AsyncSession = Depends(get_async_session)):

    create = await create_new_solution(request_id, solution_data, current_user, session)

    return create

