from pydantic import BaseModel

from src.api.user.model import UserRoleEnum


class EmployeeInfo(BaseModel):
    id: int
    name: str
    email: str
    role: UserRoleEnum
    salary: int
