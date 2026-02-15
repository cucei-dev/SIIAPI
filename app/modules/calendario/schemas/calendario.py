from pydantic import field_validator
from sqlmodel import SQLModel


class CalendarioBase(SQLModel):
    name: str
    siiau_id: str


class CalendarioCreate(CalendarioBase):
    pass


class CalendarioUpdate(SQLModel):
    name: str | None
    siiau_id: str | None


class CalendarioReadMinimal(CalendarioBase):
    id: int


class CalendarioRead(CalendarioReadMinimal):
    secciones: list["SeccionReadMinimal"]

    @field_validator("secciones", mode="before")
    @classmethod
    def limit_secciones(cls, v):
        """Limit the number of secciones returned to a maximum of 10"""
        if isinstance(v, list) and len(v) > 10:
            return v[:10]
        return v
