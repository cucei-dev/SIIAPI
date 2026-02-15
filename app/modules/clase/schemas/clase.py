from datetime import time
from typing import Optional

from sqlmodel import SQLModel


class ClaseBase(SQLModel):
    sesion: int | None
    hora_inicio: time | None
    hora_fin: time | None
    dia: int | None
    seccion_id: int
    aula_id: int | None


class ClaseCreate(ClaseBase):
    pass


class ClaseUpdate(SQLModel):
    sesion: int | None
    hora_inicio: time | None
    hora_fin: time | None
    dia: int | None
    seccion_id: int | None
    aula_id: int | None


class ClaseReadMinimal(ClaseBase):
    id: int


class ClaseRead(ClaseReadMinimal):
    seccion: "SeccionReadMinimal"
    aula: Optional["AulaReadMinimal"]
