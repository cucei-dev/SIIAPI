from datetime import datetime
from typing import Optional

from pydantic import field_validator
from sqlmodel import SQLModel


class SeccionBase(SQLModel):
    name: str
    nrc: str
    cupos: int
    cupos_disponibles: int
    periodo_inicio: datetime | None
    periodo_fin: datetime | None
    centro_id: int
    materia_id: int
    profesor_id: int | None
    calendario_id: int


class SeccionCreate(SeccionBase):
    pass


class SeccionUpdate(SQLModel):
    name: str | None
    nrc: str | None
    cupos: int | None
    cupos_disponibles: int | None
    periodo_inicio: datetime | None
    periodo_fin: datetime | None
    centro_id: int | None
    materia_id: int | None
    profesor_id: int | None
    calendario_id: int | None


class SeccionReadMinimal(SeccionBase):
    id: int


class SeccionRead(SeccionReadMinimal):
    centro: "CentroUniversitarioReadMinimal"
    materia: "MateriaReadMinimal"
    profesor: Optional["ProfesorReadMinimal"]
    calendario: "CalendarioReadMinimal"
    clases: list["ClaseReadMinimal"]

    @field_validator("clases", mode="before")
    @classmethod
    def limit_clases(cls, v):
        """Limit the number of clases returned to a maximum of 10"""
        if isinstance(v, list) and len(v) > 10:
            return v[:10]
        return v
