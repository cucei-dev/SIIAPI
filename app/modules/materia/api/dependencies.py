from app.modules.materia.repositories.materia_repository import MateriaRepository
from app.modules.materia.services.materia_service import MateriaService
from app.api.dependencies.database import get_session
from sqlmodel import Session
from fastapi import Depends

def get_user_service(
    session: Session = Depends(get_session),
) -> MateriaService:
    return MateriaService(
        repository=MateriaRepository(session=session),
    )
