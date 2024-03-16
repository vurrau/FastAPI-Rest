from pydantic import BaseModel


class RequestCreate(BaseModel):
    title: str
    description: str
