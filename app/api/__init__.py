from fastapi import APIRouter
from .routes import router as router_v1

router = APIRouter()

router.include_router(router_v1, prefix="/v1")
