from .edificio import EdificioBase, EdificioCreate, EdificioRead, EdificioUpdate
from app.modules.centro.schemas.centro import CentroUniversitarioReadMinimal
from app.modules.aula.schemas.aula import AulaReadMinimal

EdificioRead.model_rebuild()

__all__ = [
    "EdificioBase",
    "EdificioCreate",
    "EdificioRead",
    "EdificioUpdate",
]
