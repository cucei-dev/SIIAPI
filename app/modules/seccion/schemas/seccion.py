from sqlmodel import SQLModel
from datetime import datetime
from typing import Optional

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

class SeccionUpdate(SeccionBase):
    pass

class SeccionReadMinimal(SeccionBase):
    id: int

class SeccionRead(SeccionReadMinimal):
    centro: "CentroUniversitarioReadMinimal"
    materia: "MateriaReadMinimal"
    profesor: Optional["ProfesorReadMinimal"]
    calendario: "CalendarioReadMinimal"
    clases: list["ClaseReadMinimal"]
