from app.modules.seccion.schemas.seccion import SeccionReadMinimal

from .calendario import (CalendarioBase, CalendarioCreate, CalendarioRead,
                         CalendarioUpdate)

CalendarioRead.model_rebuild()

__all__ = [
    "CalendarioBase",
    "CalendarioCreate",
    "CalendarioRead",
    "CalendarioUpdate",
]
