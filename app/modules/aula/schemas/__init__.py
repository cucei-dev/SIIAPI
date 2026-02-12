from .aula import AulaBase, AulaCreate, AulaRead, AulaUpdate
from app.modules.edificio.schemas.edificio import EdificioReadMinimal
from app.modules.clase.schemas.clase import ClaseReadMinimal

AulaRead.model_rebuild()

__all__ = [
    "AulaBase",
    "AulaCreate",
    "AulaRead",
    "AulaUpdate",
]
