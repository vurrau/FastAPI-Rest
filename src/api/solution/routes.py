from fastapi import APIRouter, Depends

from src.api.solution.logic import SolutionService
from src.api.user.model import User
from src.services.manager import current_manager, current_employee
from src.api.solution.schema import SolutionInfo


solution = APIRouter(
    prefix="/solution",
    tags=["solution"]
)


@solution.post("/create", response_model=SolutionInfo)
async def create_solution(request_id: int, solution_data: str, current_user: User = Depends(current_employee)):
    result = await SolutionService.create_new_solution(request_id, solution_data, current_user)

    return result


@solution.delete("/")
async def delete_solution(solution_id: int, current_user: User = Depends(current_manager)):
    result = await SolutionService.delete_one_solution(solution_id)

    return result

