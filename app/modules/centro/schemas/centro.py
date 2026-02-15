from pydantic import field_validator
from sqlmodel import SQLModel


class CentroUniversitarioBase(SQLModel):
    name: str
    siiau_id: str


class CentroUniversitarioCreate(CentroUniversitarioBase):
    pass


class CentroUniversitarioUpdate(SQLModel):
    name: str | None
    siiau_id: str | None


class CentroUniversitarioReadMinimal(CentroUniversitarioBase):
    id: int


class CentroUniversitarioRead(CentroUniversitarioReadMinimal):
    secciones: list["SeccionReadMinimal"]
    edificios: list["EdificioReadMinimal"]

    @field_validator("secciones", "edificios", mode="before")
    @classmethod
    def limit_lists(cls, v):
        """Limit the number of items returned to a maximum of 10"""
        if isinstance(v, list) and len(v) > 10:
            return v[:10]
        return v
