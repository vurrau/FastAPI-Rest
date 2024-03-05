from fastapi import FastAPI

from src.api.schemas import UserRead, UserCreate
from src.api.manager import fastapi_users
from src.db.config import auth_backend

from src.api.router.admin import admin
from src.api.router.staff import staff
from src.api.router.user import user

app = FastAPI()


app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(admin)
app.include_router(staff)
app.include_router(user)


