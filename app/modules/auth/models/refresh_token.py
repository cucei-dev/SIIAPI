from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from pydantic import ConfigDict

class RefreshToken(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(index=True, foreign_key="user.id", ondelete="CASCADE")

    token_hash: str = Field(index=True, unique=True)
    jti: str = Field(index=True, unique=True)

    created_at: datetime = Field(default_factory=datetime.now())
    expires_at: datetime | None = Field(default=None, nullable=True)
    is_active: bool = Field(default=True)

    user_agent: str | None = Field(default=None, nullable=True)
    ip_address: str | None = Field(default=None, nullable=True)

    user: "User" = Relationship(back_populates="refresh_tokens")

    model_config = ConfigDict(from_attributes=True)
