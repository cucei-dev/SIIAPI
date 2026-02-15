from sqlmodel import SQLModel

class SeccionSiiau(SQLModel):
    NRC: str
    Clave: str
    Materia: str
    Sec: str
    CR: int
    CUP: int
    DIS: int
    Profesor: str | None
    SesionNum: str | None
    Horas: str | None
    Dias: str | None
    Edificio: str | None
    Aula: str | None
    Periodo: str | None
