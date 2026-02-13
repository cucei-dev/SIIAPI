from sqlmodel import SQLModel

class AulaBase(SQLModel):
    name: str
    edificio_id: int

class AulaCreate(AulaBase):
    pass

class AulaUpdate(SQLModel):
    name: str | None
    edificio_id: int | None

class AulaReadMinimal(AulaBase):
    id: int

class AulaRead(AulaReadMinimal):
    edificio: "EdificioReadMinimal"
    clases: list["ClaseReadMinimal"]
