from sqlmodel import SQLModel, Field, Time, Relationship
from pydantic import ConfigDict

class Clase(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    sesion: int | None = Field(default=None, nullable=True)
    hora_inicio: Time | None = Field(default=None, nullable=True)
    hora_fin: Time | None = Field(default=None, nullable=True)
    dias: list[int] | None = Field(default=None, nullable=True)

    seccion_id: int = Field(index=True, foreign_key="seccion.id", ondelete="CASCADE")
    aula_id: int | None = Field(index=True, foreign_key="aula.id", ondelete="CASCADE", default=None, nullable=True)

    seccion: "Seccion" = Relationship(back_populates="clases")
    aula: "Aula" = Relationship(back_populates="clases")

    model_config = ConfigDict(from_attributes=True)
