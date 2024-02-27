from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, TIMESTAMP, func, JSON
from sqlalchemy.orm import relationship

from src.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    registered_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    role_id = Column(Integer, ForeignKey('roles.id'))

    role = relationship("Role", back_populates="users")


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    users = relationship("User", back_populates="role")




