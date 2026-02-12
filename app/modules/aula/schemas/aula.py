from sqlmodel import SQLModel

class AulaBase(SQLModel):
    name: str
    edificio_id: int

class AulaCreate(AulaBase):
    pass

class AulaUpdate(AulaBase):
    pass

class AulaReadMinimal(AulaBase):
    id: int

class AulaRead(AulaReadMinimal):
    edificio: "EdificioReadMinimal"
    clases: list["ClaseReadMinimal"]
