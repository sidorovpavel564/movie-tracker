import uuid

import uvicorn
from fastapi import FastAPI
from fastapi_users import FastAPIUsers

from src.users.auth import auth_backend
from src.users.database import User
from src.users.manager import get_user_manager
from src.users.schemas import UserCreate
from src.users.schemas import UserRead

from src.movies.router import router as movies_router

app = FastAPI()

fastapi_users = FastAPIUsers[User, uuid.UUID](
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

app.include_router(
    movies_router,
)

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
