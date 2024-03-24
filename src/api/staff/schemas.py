from pydantic import BaseModel

from src.api.user.model import UserRoleEnum


class UserInfo(BaseModel):
    id: int
    name: str
    email: str


class EmployeeInfo(BaseModel):
    id: int
    name: str
    email: str
    # role: UserRoleEnum
