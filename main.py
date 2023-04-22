import logging
import uvicorn
from fastapi_users import FastAPIUsers
from starlette.middleware.cors import CORSMiddleware

from src.auth.config import auth_backend
from src.auth.manager import get_user_manager
from src.auth.models import User
from src.schemas.user_schemas import UserRead, UserCreate
from fastapi import FastAPI, Depends
from datetime import datetime as dt
from src.recipe.router import router as recipe_router
from src.db.redis.settings import start_redis
from src.services.settings import ORIGINS

app = FastAPI(
    title="Cooking_portal"
)

logging.basicConfig(
    level=logging.DEBUG,
    filename="log/fastapi_log.log"
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)


app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/api/v1/auth/jwt",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/api/v1/auth",
    tags=["auth"],
)
app.include_router(
    recipe_router,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type"],
)


current_user = fastapi_users.current_user()


@app.get("/api/v1/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.nickname}"


@app.on_event("startup")
async def on_startup():
    logging.log(
        logging.INFO,
        f"{dt.now()}: server up...",
    )
    await start_redis()


@app.on_event("shutdown")
async def on_shutdown():
    logging.log(
        logging.INFO,
        f"{dt.now()}: server down... ",
    )

if __name__ == '__main__':
    uvicorn.run(
        "__main__:app",
        reload=True,
    )
