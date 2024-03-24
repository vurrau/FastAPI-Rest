from typing import Optional

from fastapi_users import schemas
from prompt_toolkit import enums
from pydantic import BaseModel

from src.api.user.model import UserRoleEnum


class UserRead(schemas.BaseUser[int]):
    id: int
    email: str
    name: str
    role: UserRoleEnum
    salary: int
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False


class UserFull(BaseModel):
    id: int
    email: str
    name: str
    role: UserRoleEnum
    salary: int


class UserInfo(BaseModel):
    name: str


class EmployeeInfo(BaseModel):
    name: str
    email: str


class UserCreate(schemas.BaseUserCreate):
    name: str
    email: str
    password: str

