from sqlmodel import SQLModel

class CentroUniversitarioBase(SQLModel):
    name: str
    siiau_id: str

class CentroUniversitarioCreate(CentroUniversitarioBase):
    pass

class CentroUniversitarioUpdate(SQLModel):
    name: str | None
    siiau_id: str | None

class CentroUniversitarioReadMinimal(CentroUniversitarioBase):
    id: int

class CentroUniversitarioRead(CentroUniversitarioReadMinimal):
    secciones: list["SeccionReadMinimal"]
    edificios: list["EdificioReadMinimal"]
