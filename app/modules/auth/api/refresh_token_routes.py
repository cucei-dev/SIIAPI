from fastapi import APIRouter, Depends, Query, status

from app.api.dependencies.auth import user_is_superuser
from app.api.schemas import Pagination
from app.modules.auth.schemas import RefreshTokenCreate, RefreshTokenRead
from app.modules.auth.services.refresh_token_service import RefreshTokenService
from app.modules.users.models import User

from .dependencies import get_refresh_token_service

router = APIRouter()


@router.post("/", response_model=RefreshTokenRead, status_code=status.HTTP_201_CREATED)
async def create_refresh_token(
    data: RefreshTokenCreate,
    service: RefreshTokenService = Depends(get_refresh_token_service),
    user: User = Depends(user_is_superuser),
):
    return service.create_refresh_token(data)


@router.get("/{refresh_token_jti}", response_model=RefreshTokenRead)
async def get_refresh_token(
    refresh_token_jti: str,
    service: RefreshTokenService = Depends(get_refresh_token_service),
    user: User = Depends(user_is_superuser),
):
    return service.get_refresh_token(refresh_token_jti)


@router.get("/", response_model=Pagination[RefreshTokenRead])
async def list_refresh_tokens(
    skip: int = 0,
    limit: int = Query(default=100, ge=1, le=100),
    service: RefreshTokenService = Depends(get_refresh_token_service),
    user: User = Depends(user_is_superuser),
):
    refresh_tokens, total = service.list_refresh_tokens(
        skip=skip,
        limit=limit,
    )
    return Pagination(
        total=total,
        results=refresh_tokens,
    )


@router.delete("/{refresh_token_jti}", status_code=status.HTTP_204_NO_CONTENT)
async def soft_delete_refresh_token(
    refresh_token_jti: str,
    service: RefreshTokenService = Depends(get_refresh_token_service),
    user: User = Depends(user_is_superuser),
):
    service.delete_refresh_token(refresh_token_jti)


@router.delete("/{refresh_token_jti}/hard", status_code=status.HTTP_204_NO_CONTENT)
async def delete_refresh_token(
    refresh_token_jti: str,
    service: RefreshTokenService = Depends(get_refresh_token_service),
    user: User = Depends(user_is_superuser),
):
    service.hard_delete_refresh_token(refresh_token_jti)
