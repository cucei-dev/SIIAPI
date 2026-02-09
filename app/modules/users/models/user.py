from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from pydantic import ConfigDict

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    email: str = Field(index=True, unique=True, regex=r"^[\w\.-]+@[\w\.-]+\.\w+$")
    password: str

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    last_login: datetime | None = Field(default=None, nullable=True)

    is_active: bool = Field(default=False)
    is_superuser: bool = Field(default=False)
    is_staff: bool = Field(default=False)

    model_config = ConfigDict(from_attributes=True)
