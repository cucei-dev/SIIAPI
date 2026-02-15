from sqlmodel import SQLModel
from pydantic import field_validator

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
    
    @field_validator('clases', mode='before')
    @classmethod
    def limit_clases(cls, v):
        """Limit the number of clases returned to a maximum of 10"""
        if isinstance(v, list) and len(v) > 10:
            return v[:10]
        return v
