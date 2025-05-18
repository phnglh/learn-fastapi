from fastapi import APIRouter

from src.routes import item
from src.routes import user
api_router = APIRouter()
api_router.include_router(item.router)
api_router.include_router(user.router)


