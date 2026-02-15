from pydantic import ConfigDict
from sqlmodel import Field, Relationship, SQLModel


class Materia(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    creditos: int
    clave: str = Field(index=True, unique=True)

    secciones: list["Seccion"] = Relationship(
        back_populates="materia", cascade_delete=True
    )

    model_config = ConfigDict(from_attributes=True)
