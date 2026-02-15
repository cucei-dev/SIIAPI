from pydantic import EmailStr
from sqlmodel import SQLModel


class LoginData(SQLModel):
    email: EmailStr
    password: str
    remember_me: bool = False
    user_agent: str | None = None
    ip_address: str | None = None
    audience: str | None = None


class LoginResponse(SQLModel):
    access_token: str
    access_token_expires_at: int
    refresh_token: str | None = None
    refresh_token_expires_at: int | None = None


class RefreshTokenRequest(SQLModel):
    refresh_token: str
    user_agent: str | None = None
    ip_address: str | None = None
    audience: str | None = None
