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
