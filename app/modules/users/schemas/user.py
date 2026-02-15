from datetime import datetime
from typing import Optional

from pydantic import EmailStr
from sqlmodel import SQLModel


class UserBase(SQLModel):
    name: str
    email: EmailStr
    is_active: bool = False
    is_superuser: bool = False
    is_staff: bool = False
    is_2fa_enabled: bool = False
    quit_tax: bool = False
    quit_comission: bool = False


class UserCreate(UserBase):
    password: str


class UserAllowedUpdate(SQLModel):
    name: str | None = None
    email: EmailStr | None = None
    password: str | None = None
    is_2fa_enabled: bool | None = None


class UserReadMinimal(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime
    last_login: datetime | None = None


class UserRead(UserReadMinimal):
    refresh_tokens: list["RefreshTokenReadMinimal"] = []


class UserUpdate(UserAllowedUpdate):
    is_active: bool | None = None
    is_superuser: bool | None = None
    is_staff: bool | None = None
    quit_tax: bool | None = None
    quit_comission: bool | None = None


class UserAllowedCreate(SQLModel):
    name: str | None = None
    email: EmailStr | None = None
    password: str | None = None
