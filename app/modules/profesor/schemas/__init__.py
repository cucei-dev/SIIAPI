from app.modules.seccion.schemas.seccion import SeccionReadMinimal

from .profesor import (ProfesorBase, ProfesorCreate, ProfesorRead,
                       ProfesorUpdate)

ProfesorRead.model_rebuild()

__all__ = [
    "ProfesorBase",
    "ProfesorCreate",
    "ProfesorRead",
    "ProfesorUpdate",
]
