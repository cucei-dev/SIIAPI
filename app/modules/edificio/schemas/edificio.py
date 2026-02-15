from pydantic import field_validator
from sqlmodel import SQLModel


class EdificioBase(SQLModel):
    name: str
    centro_id: int


class EdificioCreate(EdificioBase):
    pass


class EdificioUpdate(SQLModel):
    name: str | None
    centro_id: int | None


class EdificioReadMinimal(EdificioBase):
    id: int


class EdificioRead(EdificioReadMinimal):
    centro: "CentroUniversitarioReadMinimal"
    aulas: list["AulaReadMinimal"]

    @field_validator("aulas", mode="before")
    @classmethod
    def limit_aulas(cls, v):
        """Limit the number of aulas returned to a maximum of 10"""
        if isinstance(v, list) and len(v) > 10:
            return v[:10]
        return v
