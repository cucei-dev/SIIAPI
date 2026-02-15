from pydantic import ConfigDict
from sqlmodel import Field, Relationship, SQLModel


class Aula(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str

    edificio_id: int = Field(index=True, foreign_key="edificio.id", ondelete="CASCADE")

    edificio: "Edificio" = Relationship(back_populates="aulas")

    clases: list["Clase"] = Relationship(back_populates="aula", cascade_delete=True)

    model_config = ConfigDict(from_attributes=True)
