from fastapi import APIRouter

from .routes import router as router_v1
from .schemas import Info

router = APIRouter()


@router.get("/", response_model=Info)
async def get_info():
    return Info()


router.include_router(router_v1, prefix="/v1")
