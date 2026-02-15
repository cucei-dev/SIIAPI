from datetime import datetime

from pydantic import ConfigDict
from sqlmodel import Field, Relationship, SQLModel


class Seccion(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    nrc: str
    cupos: int
    cupos_disponibles: int
    periodo_inicio: datetime | None = Field(default=None, nullable=True)
    periodo_fin: datetime | None = Field(default=None, nullable=True)

    centro_id: int = Field(
        index=True, foreign_key="centrouniversitario.id", ondelete="CASCADE"
    )
    materia_id: int = Field(index=True, foreign_key="materia.id", ondelete="CASCADE")
    profesor_id: int | None = Field(
        index=True,
        foreign_key="profesor.id",
        ondelete="CASCADE",
        default=None,
        nullable=True,
    )
    calendario_id: int = Field(
        index=True, foreign_key="calendario.id", ondelete="CASCADE"
    )

    centro: "CentroUniversitario" = Relationship(back_populates="secciones")
    materia: "Materia" = Relationship(back_populates="secciones")
    profesor: "Profesor" = Relationship(back_populates="secciones")
    calendario: "Calendario" = Relationship(back_populates="secciones")

    clases: list["Clase"] = Relationship(back_populates="seccion", cascade_delete=True)

    model_config = ConfigDict(from_attributes=True)
