from pydantic import BaseModel

from src.api.user.model import UserRoleEnum


class EmployeeInfo(BaseModel):
    name: str
    email: str


class EmployeeInfoBasic(BaseModel):
    id: int
    name: str
    email: str
    role: UserRoleEnum


class EmployeeInfoFull(BaseModel):
    id: int
    name: str
    email: str
    role: UserRoleEnum
    salary: int
