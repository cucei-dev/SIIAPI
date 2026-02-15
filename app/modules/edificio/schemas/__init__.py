from app.modules.aula.schemas.aula import AulaReadMinimal
from app.modules.centro.schemas.centro import CentroUniversitarioReadMinimal

from .edificio import (EdificioBase, EdificioCreate, EdificioRead,
                       EdificioUpdate)

EdificioRead.model_rebuild()

__all__ = [
    "EdificioBase",
    "EdificioCreate",
    "EdificioRead",
    "EdificioUpdate",
]
