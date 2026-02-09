from fastapi import APIRouter, Depends, status
from .refresh_token_routes import router as refresh_token_router
from app.modules.auth.schemas import LoginResponse, LoginData, ToptActivationResponse, Verify2FA, RefreshTokenRequest, ToptConfirmationRequest, APITokenCreate
from .dependencies import get_auth_service
from app.modules.auth.services.auth_service import AuthService
from app.modules.users.schemas import UserRead, UserAllowedUpdate, UserAllowedCreate
from app.modules.users.schemas.user import UserReadMinimal
from app.api.dependencies.auth import get_current_user_strict
from app.modules.users.models import User
from app.modules.users.api.dependencies import get_user_service
from app.modules.users.services.user_service import UserService

router = APIRouter()

@router.post("/login", response_model=LoginResponse)
async def login(
    data: LoginData,
    service: AuthService = Depends(get_auth_service),
):
    return service.login(data)

@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    data: RefreshTokenRequest,
    service: AuthService = Depends(get_auth_service),
    user: User = Depends(get_current_user_strict),
):
    return service.logout(data, user)

router.include_router(refresh_token_router, prefix="/refresh-tokens")
