from .calendario import CalendarioBase, CalendarioCreate, CalendarioRead, CalendarioUpdate
from app.modules.seccion.schemas.seccion import SeccionReadMinimal

CalendarioRead.model_rebuild()

__all__ = [
    "CalendarioBase",
    "CalendarioCreate",
    "CalendarioRead",
    "CalendarioUpdate",
]
