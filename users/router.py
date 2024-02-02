from fastapi import APIRouter

from users.schemas import UserCreate, UserRead
from users.users import auth_backend, fastapi_users


user_router = APIRouter()


user_router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    tags=["auth"]
)
user_router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    tags=["auth"],
)
