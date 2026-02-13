from app.modules.aula.repositories.aula_repository import AulaRepository
from app.modules.aula.services.aula_service import AulaService
from app.api.dependencies.database import get_session
from sqlmodel import Session
from fastapi import Depends

def get_user_service(
    session: Session = Depends(get_session),
) -> AulaService:
    return AulaService(
        repository=AulaRepository(session=session),
    )
