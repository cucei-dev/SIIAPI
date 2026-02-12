from .profesor import ProfesorBase, ProfesorCreate, ProfesorRead, ProfesorUpdate
from app.modules.seccion.schemas.seccion import SeccionReadMinimal

ProfesorRead.model_rebuild()

__all__ = [
    "ProfesorBase",
    "ProfesorCreate",
    "ProfesorRead",
    "ProfesorUpdate",
]
