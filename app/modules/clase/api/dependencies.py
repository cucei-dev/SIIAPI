from app.modules.clase.repositories.clase_repository import ClaseRepository
from app.modules.clase.services.clase_service import ClaseService
from app.api.dependencies.database import get_session
from sqlmodel import Session
from fastapi import Depends
from app.modules.seccion.repositories.seccion_repository import SeccionRepository
from app.modules.aula.repositories.aula_repository import AulaRepository

def get_clase_service(
    session: Session = Depends(get_session),
) -> ClaseService:
    return ClaseService(
        repository=ClaseRepository(session=session),
        seccion_repository=SeccionRepository(session=session),
        aula_repository=AulaRepository(session=session),
    )
