from sqlmodel import SQLModel

class EdificioBase(SQLModel):
    name: str
    centro_id: int

class EdificioCreate(EdificioBase):
    pass

class EdificioUpdate(EdificioBase):
    pass

class EdificioReadMinimal(EdificioBase):
    id: int

class EdificioRead(EdificioReadMinimal):
    centro: "CentroUniversitarioReadMinimal"
    aulas: list["AulaReadMinimal"]
