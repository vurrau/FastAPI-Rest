from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, TIMESTAMP, func, JSON
from sqlalchemy.orm import relationship, Mapped, mapped_column

from src.db.base import Base

from enum import Enum
from sqlalchemy.dialects.postgresql import ENUM as PgEnum


class UserRoleEnum(Enum):
    USER = 'USER'
    STAFF = 'STAFF'
    ADMIN = 'ADMIN'


class User(SQLAlchemyBaseUserTable[int], Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(length=320), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(length=1024), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    role: Mapped[str] = mapped_column(
        PgEnum(UserRoleEnum, name='user_role_enum', create_type=False), nullable=False, default=UserRoleEnum.USER)




