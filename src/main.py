from fastapi import FastAPI, Depends, APIRouter
from fastapi_users import FastAPIUsers
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import undefer, selectinload, defer

from src.api.manager import get_user_manager
from src.api.models import User
from src.api.schemas import UserRead, UserCreate
from src.api.manager import fastapi_users
from src.db.base import get_async_session
from src.db.config import auth_backend

from src.api.crud import crud

app = FastAPI()


app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/register",
    tags=["register"],
)

app.include_router(crud)

