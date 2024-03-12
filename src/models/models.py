from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.core.db.base import Base

from enum import Enum
from sqlalchemy.dialects.postgresql import ENUM as Pg_Enum


class UserRoleEnum(Enum):
    USER = 'USER'
    STAFF = 'STAFF'
    ADMIN = 'ADMIN'


class User(SQLAlchemyBaseUserTable[int], Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(length=30), nullable=False)
    email: Mapped[str] = mapped_column(String(length=320), unique=True, index=True, nullable=False)
    role: Mapped[str] = mapped_column(
        Pg_Enum(UserRoleEnum, name='role_enum'), nullable=False, default=UserRoleEnum.USER)
    salary: Mapped[int] = mapped_column(Integer, default=0, nullable=True)
    hashed_password: Mapped[str] = mapped_column(String(length=1024), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)





