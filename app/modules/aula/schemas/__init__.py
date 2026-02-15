from app.modules.clase.schemas.clase import ClaseReadMinimal
from app.modules.edificio.schemas.edificio import EdificioReadMinimal

from .aula import AulaBase, AulaCreate, AulaRead, AulaUpdate

AulaRead.model_rebuild()

__all__ = [
    "AulaBase",
    "AulaCreate",
    "AulaRead",
    "AulaUpdate",
]
