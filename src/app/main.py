from fastapi import APIRouter

from src.routes import item

api_router = APIRouter()
api_router.include_router(item.router)

