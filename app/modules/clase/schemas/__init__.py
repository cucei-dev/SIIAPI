from .clase import ClaseBase, ClaseCreate, ClaseRead, ClaseUpdate
from app.modules.seccion.schemas.seccion import SeccionReadMinimal
from app.modules.aula.schemas.aula import AulaReadMinimal

ClaseRead.model_rebuild()

__all__ = [
    "ClaseBase",
    "ClaseCreate",
    "ClaseRead",
    "ClaseUpdate",
]
