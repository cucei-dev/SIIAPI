from fastapi import APIRouter
from app.modules.users.api.routes import router as users_router
from app.modules.auth.api.routes import router as auth_router

router = APIRouter()

router.include_router(auth_router, prefix="/auth", tags=["Auth"])
router.include_router(users_router, prefix="/users", tags=["Users"])
