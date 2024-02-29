from src.main import app
from fastapi_users import FastAPIUsers

from src.api.models import User
from src.api.manager import get_user_manager
from src.api.schemas import UserRead, UserCreate
from src.db.config import auth_backend


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)