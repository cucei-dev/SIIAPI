from sqlmodel import SQLModel, Field, Relationship
from pydantic import ConfigDict

class Calendario(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    siiau_id: str = Field(index=True, unique=True)

    secciones: list["Seccion"] = Relationship(back_populates="calendario", cascade_delete=True)

    model_config = ConfigDict(from_attributes=True)
