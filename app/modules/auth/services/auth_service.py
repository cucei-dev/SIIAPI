from datetime import datetime

from app.core.exceptions import (BadRequestException, ForbiddenException,
                                 UnauthorizedException)
from app.core.security import (check_token, create_access_token,
                               create_refresh_token, verify_password)
from app.modules.auth.schemas import (AccessTokenData, LoginData,
                                      LoginResponse, RefreshTokenCreate,
                                      RefreshTokenData, RefreshTokenRequest,
                                      Token)
from app.modules.users.models import User
from app.modules.users.repositories.user_repository import UserRepository

from .refresh_token_service import RefreshTokenService


class AuthService:
    def __init__(
        self,
        refresh_token_service: RefreshTokenService,
        user_repository: UserRepository,
    ):
        self.refresh_token_service = refresh_token_service
        self.user_repository = user_repository

    def login(self, data: LoginData) -> LoginResponse:
        users, total = self.user_repository.list({"email": data.email})

        if not total:
            verify_password(data.password)
            raise BadRequestException("Invalid email or password.")

        user = users[0]

        if not verify_password(data.password, user.password):
            raise BadRequestException("Invalid email or password.")

        if not user.is_active:
            raise ForbiddenException("User is inactive.")

        user.last_login = datetime.now()
        self.user_repository.update(user)

        return self.create_tokens(
            login_data=data,
            user=user,
        )

    def create_tokens(
        self,
        login_data: LoginData,
        user: User,
        temporary: bool = False,
        refresh: bool = True,
        refresh_token: Token | None = None,
    ) -> LoginResponse:
        if refresh and not refresh_token:
            refresh_token = create_refresh_token(
                RefreshTokenData(
                    sub=user.email,
                ),
            )

            refresh_token_data = RefreshTokenCreate(
                user_id=user.id,
                token_hash=refresh_token.token_hash,
                jti=refresh_token.data.jti,
                created_at=datetime.fromtimestamp(refresh_token.data.iat),
                expires_at=datetime.fromtimestamp(refresh_token.data.exp),
                user_agent=login_data.user_agent,
                ip_address=login_data.ip_address,
            )

            self.refresh_token_service.create_refresh_token(refresh_token_data)

        access_token = create_access_token(
            AccessTokenData(
                sub=user.email,
                is_superuser=user.is_superuser,
                is_staff=user.is_staff,
                aud=login_data.audience,
                refresh_jti=refresh_token.data.jti if refresh_token else None,
                type="temporary" if temporary else "access",
            )
        )

        return LoginResponse(
            access_token=access_token.token,
            access_token_expires_at=access_token.data.exp,
            refresh_token=refresh_token.token if not temporary else None,
            refresh_token_expires_at=refresh_token.data.exp if not temporary else None,
        )

    def logout(self, data: RefreshTokenRequest, user: User) -> None:
        token = check_token(data.refresh_token, "refresh")

        if not token:
            raise UnauthorizedException("Invalid refresh token.")

        refresh_token = self.refresh_token_service.get_refresh_token(token.get("jti"))

        if not refresh_token.is_active:
            raise UnauthorizedException("Refresh token is inactive.")

        if (
            refresh_token.user_agent != data.user_agent
            or refresh_token.ip_address != data.ip_address
        ):
            raise UnauthorizedException("Refresh token is invalid.")

        if refresh_token.expires_at < datetime.now():
            raise UnauthorizedException("Refresh token is expired.")

        if refresh_token.created_at > datetime.now():
            raise UnauthorizedException("Refresh token is not yet valid.")

        if not refresh_token.user.is_active:
            raise ForbiddenException("User is inactive.")

        if not verify_password(data.refresh_token, refresh_token.token_hash):
            raise UnauthorizedException("Invalid refresh token hash.")

        if user.id != refresh_token.user_id:
            raise UnauthorizedException("Refresh token does not belong to ehe user.")

        self.refresh_token_service.delete_refresh_token(refresh_token.jti)

        return None
