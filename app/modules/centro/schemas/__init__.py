from .centro import CentroUniversitarioBase, CentroUniversitarioCreate, CentroUniversitarioRead, CentroUniversitarioUpdate
from app.modules.seccion.schemas.seccion import SeccionReadMinimal
from app.modules.edificio.schemas.edificio import EdificioReadMinimal

CentroUniversitarioRead.model_rebuild()

__all__ = [
    "CentroUniversitarioBase",
    "CentroUniversitarioCreate",
    "CentroUniversitarioRead",
    "CentroUniversitarioUpdate",
]
