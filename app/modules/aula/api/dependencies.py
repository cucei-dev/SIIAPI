from app.modules.aula.repositories.aula_repository import AulaRepository
from app.modules.aula.services.aula_service import AulaService
from app.api.dependencies.database import get_session
from sqlmodel import Session
from fastapi import Depends
from app.modules.edificio.repositories.edificio_repository import EdificioRepository

def get_aula_service(
    session: Session = Depends(get_session),
) -> AulaService:
    return AulaService(
        repository=AulaRepository(session=session),
        edificio_repository=EdificioRepository(session=session),
    )
