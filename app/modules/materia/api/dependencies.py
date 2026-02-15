from fastapi import Depends
from sqlmodel import Session

from app.api.dependencies.database import get_session
from app.modules.materia.repositories.materia_repository import \
    MateriaRepository
from app.modules.materia.services.materia_service import MateriaService


def get_materia_service(
    session: Session = Depends(get_session),
) -> MateriaService:
    return MateriaService(
        repository=MateriaRepository(session=session),
    )
