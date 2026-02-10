from sqlmodel import SQLModel, Field, Relationship
from pydantic import ConfigDict

class Profesor(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)

    secciones: list["Seccion"] = Relationship(back_populates="profesor", cascade_delete=True)

    model_config = ConfigDict(from_attributes=True)
