from datetime import datetime
from sqlmodel import SQLModel

class RefreshTokenBase(SQLModel):
    user_id: int
    token_hash: str
    jti: str
    created_at: datetime
    expires_at: datetime
    user_agent: str | None
    ip_address: str | None

class RefreshTokenCreate(RefreshTokenBase):
    pass

class RefreshTokenUpdate(SQLModel):
    is_active: bool = True

class RefreshTokenReadMinimal(RefreshTokenBase):
    id: int

class RefreshTokenRead(RefreshTokenReadMinimal):
    user: "UserReadMinimal"
