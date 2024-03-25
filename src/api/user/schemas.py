
from fastapi_users import schemas
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


class UserCreate(schemas.BaseUserCreate):
    name: str
    email: str
    password: str


class UserInfoBasic(BaseModel):
    id: int
    email: str
    name: str


class UserInfo(BaseModel):
    name: str





