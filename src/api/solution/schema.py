from pydantic import BaseModel


class SolutionCreate(BaseModel):
    description: str
