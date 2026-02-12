from sqlmodel import SQLModel

class CalendarioBase(SQLModel):
    name: str
    siiau_id: str

class CalendarioCreate(CalendarioBase):
    pass

class CalendarioUpdate(CalendarioBase):
    pass

class CalendarioReadMinimal(CalendarioBase):
    id: int

class CalendarioRead(CalendarioReadMinimal):
    secciones: list["SeccionReadMinimal"]
