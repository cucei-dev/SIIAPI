from .materia import MateriaBase, MateriaCreate, MateriaRead, MateriaUpdate
from app.modules.seccion.schemas.seccion import SeccionReadMinimal

MateriaRead.model_rebuild()

__all__ = [
    "MateriaBase",
    "MateriaCreate",
    "MateriaRead",
    "MateriaUpdate",
]
