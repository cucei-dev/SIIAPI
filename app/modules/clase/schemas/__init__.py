from app.modules.aula.schemas.aula import AulaReadMinimal
from app.modules.seccion.schemas.seccion import SeccionReadMinimal

from .clase import ClaseBase, ClaseCreate, ClaseRead, ClaseUpdate

ClaseRead.model_rebuild()

__all__ = [
    "ClaseBase",
    "ClaseCreate",
    "ClaseRead",
    "ClaseUpdate",
]
