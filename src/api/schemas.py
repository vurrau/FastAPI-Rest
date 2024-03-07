from typing import Optional

from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    id: int
    email: str
    name: str
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False


class UserCreate(schemas.BaseUserCreate):
    name: str
    email: str
    password: str

