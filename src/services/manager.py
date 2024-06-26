from typing import Optional

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, IntegerIDMixin, schemas, models, exceptions, FastAPIUsers

from src.api.user.model import User
from src.services.utils import get_user_db

from src.core.config import SECRET_MANAGER
from src.core.db.config import auth_backend


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = SECRET_MANAGER
    verification_token_secret = SECRET_MANAGER

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

    async def create(
            self,
            user_create: schemas.UC,
            safe: bool = False,
            request: Optional[Request] = None,
    ) -> models.UP:
        await self.validate_password(user_create.password, user_create)

        existing_user = await self.user_db.get_by_email(user_create.email)
        if existing_user is not None:
            raise exceptions.UserAlreadyExists()

        user_dict = (
            user_create.create_update_dict()
            if safe
            else user_create.create_update_dict_superuser()
        )
        password = user_dict.pop("password")
        user_dict["hashed_password"] = self.password_helper.hash(password)
        user_dict["role"] = "USER"

        created_user = await self.user_db.create(user_dict)

        await self.on_after_register(created_user, request)

        return created_user


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_manager = fastapi_users.current_user(active=True, superuser=True)
current_employee = fastapi_users.current_user(active=True, verified=True)
current_active_user = fastapi_users.current_user(active=True)
