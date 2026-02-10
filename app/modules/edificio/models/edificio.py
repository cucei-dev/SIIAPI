from sqlmodel import SQLModel, Field, Relationship
from pydantic import ConfigDict

class Edificio(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str

    centro_id: int = Field(index=True, foreign_key="centro.id", ondelete="CASCADE")

    centro: "CentroUniversitario" = Relationship(back_populates="edificios")

    aulas: list["Aula"] = Relationship(back_populates="edificio", cascade_delete=True)

    model_config = ConfigDict(from_attributes=True)
