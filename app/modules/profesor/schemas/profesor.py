from pydantic import field_validator
from sqlmodel import SQLModel


class ProfesorBase(SQLModel):
    name: str


class ProfesorCreate(ProfesorBase):
    pass


class ProfesorUpdate(SQLModel):
    name: str | None


class ProfesorReadMinimal(ProfesorBase):
    id: int


class ProfesorRead(ProfesorReadMinimal):
    secciones: list["SeccionReadMinimal"]

    @field_validator("secciones", mode="before")
    @classmethod
    def limit_secciones(cls, v):
        """Limit the number of secciones returned to a maximum of 10"""
        if isinstance(v, list) and len(v) > 10:
            return v[:10]
        return v
