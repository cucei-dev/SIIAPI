from datetime import time

from pydantic import ConfigDict
from sqlmodel import JSON, Column, Field, Relationship, SQLModel


class Clase(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    sesion: int | None = Field(default=None, nullable=True)
    hora_inicio: time | None = Field(default=None, nullable=True)
    hora_fin: time | None = Field(default=None, nullable=True)
    dia: int | None = Field(default=None, nullable=True)

    seccion_id: int = Field(index=True, foreign_key="seccion.id", ondelete="CASCADE")
    aula_id: int | None = Field(
        index=True,
        foreign_key="aula.id",
        ondelete="CASCADE",
        default=None,
        nullable=True,
    )

    seccion: "Seccion" = Relationship(back_populates="clases")
    aula: "Aula" = Relationship(back_populates="clases")

    model_config = ConfigDict(from_attributes=True)
