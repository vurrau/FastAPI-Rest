from datetime import datetime

from pydantic import BaseModel

from src.api.request.model import StatusEnum, AssigneeEnum


class RequestCreate(BaseModel):
    title: str
    description: str


class RequestInfo(BaseModel):
    id: int
    title: str
    description: str
    status: StatusEnum
    assignee: AssigneeEnum
    created_at: datetime
    user_id: int
