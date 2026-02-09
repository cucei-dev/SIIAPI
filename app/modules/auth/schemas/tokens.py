from sqlmodel import SQLModel

class AccessTokenData(SQLModel):
    sub: str
    is_superuser: bool
    is_staff: bool
    iat: int | None = None
    exp: int | None = None
    iss: str | None = None
    aud: str | None = None
    jti: str | None = None
    refresh_jti: str | None = None
    type: str = "access"

class RefreshTokenData(SQLModel):
    sub: str
    iat: int | None = None
    exp: int | None = None
    jti: str | None = None
    type: str = "refresh"

class Token(SQLModel):
    token: str
    data: AccessTokenData | RefreshTokenData
    token_hash: str | None = None
