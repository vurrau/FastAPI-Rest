from datetime import datetime

from sqlalchemy import Integer, String, Column, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ENUM as St_Enum
from enum import Enum


from src.core.db.base import Base


class StatusEnum(Enum):
    OPEN = 'Open'
    MANAGER_REVIEW = 'manager review'
    CLOSED = "Closed"


class Request(Base):
    __tablename__ = "request"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    status = Column(St_Enum(StatusEnum, name='status_enum'), nullable=False, default=StatusEnum.OPEN)
    created_at = Column(DateTime, default=datetime)
    user_id = Column(Integer, ForeignKey("user.id"))

    user = relationship("User", back_populates="request")
    solutions = relationship("Solution", back_populates="request")
