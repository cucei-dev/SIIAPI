from sqlmodel import SQLModel

class ProfesorBase(SQLModel):
    name: str

class ProfesorCreate(ProfesorBase):
    pass

class ProfesorUpdate(ProfesorBase):
    pass

class ProfesorReadMinimal(ProfesorBase):
    id: int

class ProfesorRead(ProfesorReadMinimal):
    secciones: list["SeccionReadMinimal"]
