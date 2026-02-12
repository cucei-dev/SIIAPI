from sqlmodel import SQLModel

class MateriaBase(SQLModel):
    name: str
    creditos: int
    clave: str

class MateriaCreate(MateriaBase):
    pass

class MateriaUpdate(MateriaBase):
    pass

class MateriaReadMinimal(MateriaBase):
    id: int

class MateriaRead(MateriaReadMinimal):
    secciones: list["SeccionReadMinimal"]
