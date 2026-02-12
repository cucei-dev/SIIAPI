from sqlmodel import SQLModel
from datetime import time
from typing import Optional

class ClaseBase(SQLModel):
    sesion: int | None
    hora_inicio: time | None
    hora_fin: time | None
    dia: int | None
    seccion_id: int
    aula_id: int | None

class ClaseCreate(ClaseBase):
    pass

class ClaseUpdate(ClaseBase):
    pass

class ClaseReadMinimal(ClaseBase):
    id: int

class ClaseRead(ClaseReadMinimal):
    seccion: "SeccionReadMinimal"
    aula: Optional["AulaReadMinimal"]
