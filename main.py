from app.api.routers.user import router as users_router
from app.api.routers.auth import router as auth_router
from fastapi import FastAPI

app = FastAPI()

app.include_router(users_router)
app.include_router(auth_router)


