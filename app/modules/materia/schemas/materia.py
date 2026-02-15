from pydantic import field_validator
from sqlmodel import SQLModel


class MateriaBase(SQLModel):
    name: str
    creditos: int
    clave: str


class MateriaCreate(MateriaBase):
    pass


class MateriaUpdate(SQLModel):
    name: str | None
    creditos: int | None
    clave: str | None


class MateriaReadMinimal(MateriaBase):
    id: int


class MateriaRead(MateriaReadMinimal):
    secciones: list["SeccionReadMinimal"]

    @field_validator("secciones", mode="before")
    @classmethod
    def limit_secciones(cls, v):
        """Limit the number of secciones returned to a maximum of 10"""
        if isinstance(v, list) and len(v) > 10:
            return v[:10]
        return v
