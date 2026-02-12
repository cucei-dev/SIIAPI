from .seccion import SeccionBase, SeccionCreate, SeccionRead, SeccionUpdate
from app.modules.centro.schemas.centro import CentroUniversitarioReadMinimal
from app.modules.materia.schemas.materia import MateriaReadMinimal
from app.modules.profesor.schemas.profesor import ProfesorReadMinimal
from app.modules.calendario.schemas.calendario import CalendarioReadMinimal
from app.modules.clase.schemas.clase import ClaseReadMinimal

SeccionRead.model_rebuild()

__all__ = [
    "SeccionBase",
    "SeccionCreate",
    "SeccionRead",
    "SeccionUpdate",
]
