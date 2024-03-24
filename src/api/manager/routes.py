from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.request.logic import get_all_request
from src.services.manager import fastapi_users
from src.api.user.model import User
from src.core.db.base import get_async_session

manager = APIRouter(
    prefix="/manager",
    tags=["manager"]
)




