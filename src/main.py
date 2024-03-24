from fastapi import FastAPI

from src.api.manager.routes import manager
from src.api.request.routes import request
from src.api.solution.routes import solution
from src.api.user.schemas import UserRead, UserCreate
from src.services.manager import fastapi_users
from src.core.db.config import auth_backend

from src.api.admin.routes import admin
from src.api.staff.routes import staff
from src.api.user.routes import user

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

routers = [admin, staff, user, request, solution, manager]

for router in routers:
    app.include_router(router)




