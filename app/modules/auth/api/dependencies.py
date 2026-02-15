from fastapi import Depends
from sqlmodel import Session

from app.api.dependencies.database import get_session
from app.modules.auth.repositories.refresh_token_repository import \
    RefreshTokenRepository
from app.modules.auth.services.auth_service import AuthService
from app.modules.auth.services.refresh_token_service import RefreshTokenService
from app.modules.users.repositories.user_repository import UserRepository


def get_refresh_token_service(
    session: Session = Depends(get_session),
) -> RefreshTokenService:
    return RefreshTokenService(
        repository=RefreshTokenRepository(session=session),
        user_repository=UserRepository(session=session),
    )


def get_auth_service(
    session: Session = Depends(get_session),
    refresh_token_service: RefreshTokenService = Depends(get_refresh_token_service),
):
    return AuthService(
        refresh_token_service=refresh_token_service,
        user_repository=UserRepository(session=session),
    )
