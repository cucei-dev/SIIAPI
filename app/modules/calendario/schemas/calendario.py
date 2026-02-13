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
