from sqlmodel import SQLModel, Field, Relationship
from pydantic import ConfigDict

class CentroUniversitario(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    siiau_id: str = Field(index=True, unique=True)

    secciones: list["Seccion"] = Relationship(back_populates="centro", cascade_delete=True)
    edificios: list["Edificio"] = Relationship(back_populates="centro", cascade_delete=True)

    model_config = ConfigDict(from_attributes=True)
