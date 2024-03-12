from fastapi import FastAPI

from src.schemas.schemas import UserRead, UserCreate
from src.services.manager import fastapi_users
from src.core.db.config import auth_backend

from src.api.routes.admin import admin
from src.api.routes.staff import staff
from src.api.routes.user import user

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


