from sqlmodel import SQLModel

class CentroUniversitarioBase(SQLModel):
    name: str
    siiau_id: str

class CentroUniversitarioCreate(CentroUniversitarioBase):
    pass

class CentroUniversitarioUpdate(CentroUniversitarioBase):
    pass

class CentroUniversitarioReadMinimal(CentroUniversitarioBase):
    id: int

class CentroUniversitarioRead(CentroUniversitarioReadMinimal):
    secciones: list["SeccionReadMinimal"]
    edificios: list["EdificioReadMinimal"]
