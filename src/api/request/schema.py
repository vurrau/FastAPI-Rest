from datetime import datetime

from pydantic import BaseModel

from src.api.request.model import StatusEnum, AssigneeEnum


class RequestCreate(BaseModel):
    title: str
    description: str
