import logging
import uvicorn
from fastapi_users import FastAPIUsers

from src.auth.config import auth_backend
from src.auth.manager import get_user_manager
from src.auth.models import User
from src.schemas.user_schemas import UserRead, UserCreate
from src.services import routers
from fastapi import FastAPI, Depends
from datetime import datetime as dt


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

app.include_router(routers.router)
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

current_user = fastapi_users.current_user()


@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.nickname}"


@app.on_event("startup")
async def on_startup():
    logging.log(
        logging.INFO,
        f"{dt.now()}: server up...",
    )


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
