import uuid
from typing import Union

from fastapi import Depends
from fastapi_users import (
    BaseUserManager, InvalidPasswordException, FastAPIUsers, UUIDIDMixin
)
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from db.async_database_session import get_async_session
from settings import settings
from users.models import User
from users.schemas import UserCreate


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = settings.TOKEN_SECRET
    verification_token_secret = settings.TOKEN_SECRET

    async def validate_password(
            self,
            password: str,
            user: Union[UserCreate, User],
    ) -> None:
        if len(password) < 8:
            raise InvalidPasswordException(
                reason="Password should be at least 8 characters"
            )
        if user.email in password:
            raise InvalidPasswordException(
                reason="Password should not contain e-mail"
            )


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)


async def get_user_manager(
        user_db: SQLAlchemyUserDatabase = Depends(get_user_db)
):
    yield UserManager(user_db)


bearer_transport = BearerTransport(tokenUrl="/login")


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=settings.TOKEN_SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [auth_backend])

current_active_user = fastapi_users.current_user(active=True)
