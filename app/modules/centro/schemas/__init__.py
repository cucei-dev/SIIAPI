from app.modules.edificio.schemas.edificio import EdificioReadMinimal
from app.modules.seccion.schemas.seccion import SeccionReadMinimal

from .centro import (CentroUniversitarioBase, CentroUniversitarioCreate,
                     CentroUniversitarioRead, CentroUniversitarioUpdate)

CentroUniversitarioRead.model_rebuild()

__all__ = [
    "CentroUniversitarioBase",
    "CentroUniversitarioCreate",
    "CentroUniversitarioRead",
    "CentroUniversitarioUpdate",
]
