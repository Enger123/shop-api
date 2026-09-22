from app.api.routers.user import router as users_router
from fastapi import FastAPI

app = FastAPI()

app.include_router(users_router)

