from app.modules.seccion.schemas.seccion import SeccionReadMinimal

from .materia import MateriaBase, MateriaCreate, MateriaRead, MateriaUpdate

MateriaRead.model_rebuild()

__all__ = [
    "MateriaBase",
    "MateriaCreate",
    "MateriaRead",
    "MateriaUpdate",
]
