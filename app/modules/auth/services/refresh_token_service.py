from app.core.exceptions import ConflictException, NotFoundException
from app.modules.auth.models import RefreshToken
from app.modules.auth.repositories.refresh_token_repository import \
    RefreshTokenRepository
from app.modules.auth.schemas import RefreshTokenCreate, RefreshTokenUpdate
from app.modules.users.repositories.user_repository import UserRepository


class RefreshTokenService:
    def __init__(
        self,
        repository: RefreshTokenRepository,
        user_repository: UserRepository,
    ):
        self.repository = repository
        self.user_repository = user_repository

    def create_refresh_token(self, data: RefreshTokenCreate) -> RefreshToken:
        token = RefreshToken.model_validate(data)

        if self.user_repository.get(data.user_id):
            _, exists_jti = self.repository.list({"jti": data.jti})
            _, exists_token_hash = self.repository.list({"token_hash": data.token_hash})
            if exists_jti or exists_token_hash:
                raise ConflictException("Refresh Token already exists.")

            return self.repository.create(token)

    def get_refresh_token(self, refresh_token_jti: str) -> RefreshToken:
        refresh_token, total = self.repository.list({"jti": refresh_token_jti})
        if not total:
            raise NotFoundException("Refresh Token not found.")
        return refresh_token[0]

    def list_refresh_tokens(self, **filters) -> tuple[list[RefreshToken], int]:
        return self.repository.list(filters)

    def delete_refresh_token(self, refresh_token_jti: str) -> None:
        refresh_token, total = self.repository.list({"jti": refresh_token_jti})
        if not total:
            raise NotFoundException("Refresh Token not found.")

        refresh_token[0].is_active = False
        self.repository.update(refresh_token[0])

        return None

    def hard_delete_refresh_token(self, refresh_token_jti: str) -> None:
        refresh_token, total = self.repository.list({"jti": refresh_token_jti})
        if not total:
            raise NotFoundException("Refresh Token not found.")

        self.repository.delete(refresh_token[0])

        return None
