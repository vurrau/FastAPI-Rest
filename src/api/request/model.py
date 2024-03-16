from datetime import datetime

from sqlalchemy import Integer, String, Column, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import ENUM as St_Enum
from enum import Enum

from src.core.db.base import Base


class StatusEnum(Enum):
    OPEN = 'OPEN'
    PROCESSING = 'PROCESSING'
    CLOSED = "CLOSED"


class AssigneeEnum(Enum):
    STAFF = 'STAFF'
    MANAGER = 'MANAGER'


class Request(Base):
    __tablename__ = "request"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)

    status = Column(St_Enum(StatusEnum, name='statusENUM'), nullable=False, default=StatusEnum.OPEN)
    assignee = Column(St_Enum(AssigneeEnum, name='assigneeENUM'), nullable=False, default=AssigneeEnum.STAFF)

    created_at = Column(DateTime, default=datetime)
    user_id = Column(Integer, ForeignKey("user.id"))

