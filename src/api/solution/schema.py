from datetime import datetime

from pydantic import BaseModel


class SolutionCreate(BaseModel):
    description: str


class SolutionInfo(BaseModel):
    id: int
    description: str
    username: str
    response_at: datetime
    request_id: int
