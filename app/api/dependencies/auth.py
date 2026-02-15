from datetime import datetime

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.exceptions import (ForbiddenException, NotFoundException,
                                 UnauthorizedException)
from app.core.security import check_token
from app.modules.auth.api.dependencies import get_refresh_token_service
from app.modules.auth.services.refresh_token_service import RefreshTokenService
from app.modules.users.models import User

oauth2_scheme_strict = HTTPBearer()
oauth2_scheme = HTTPBearer(auto_error=False)


def user_is_superuser(
    access_token: HTTPAuthorizationCredentials = Depends(oauth2_scheme_strict),
    service: RefreshTokenService = Depends(get_refresh_token_service),
) -> User:
    user = get_current_user_strict(access_token, service)

    if not user.is_superuser:
        raise ForbiddenException("Not enough permissions.")

    return user


def user_is_staff(
    access_token: HTTPAuthorizationCredentials = Depends(oauth2_scheme_strict),
    service: RefreshTokenService = Depends(get_refresh_token_service),
) -> User:
    user = get_current_user_strict(access_token, service)

    if not user.is_staff:
        raise ForbiddenException("Not enough permissions.")

    return user


def get_current_user_strict(
    access_token=Depends(oauth2_scheme_strict),
    service: RefreshTokenService = Depends(get_refresh_token_service),
) -> User:
    user = get_current_user(access_token, service)

    if not user:
        raise UnauthorizedException("Invalid or expired token.")

    return user


def get_current_user(
    access_token: HTTPAuthorizationCredentials = Depends(oauth2_scheme),
    service: RefreshTokenService = Depends(get_refresh_token_service),
) -> User | None:
    if not access_token:
        return None

    token = check_token(access_token.credentials, "access")

    if not token:
        return None

    existing_refresh_token = service.get_refresh_token(token.get("refresh_jti"))

    if not existing_refresh_token:
        raise UnauthorizedException("Refresh token not found.")

    if not existing_refresh_token.is_active:
        raise UnauthorizedException("Refresh token is inactive.")

    if existing_refresh_token.expires_at < datetime.now():
        raise UnauthorizedException("Refresh token has expired.")

    if existing_refresh_token.created_at > datetime.now():
        raise UnauthorizedException("Refresh token is not yet valid.")

    if not existing_refresh_token.user.is_active:
        raise ForbiddenException("User is inactive.")

    return existing_refresh_token.user
