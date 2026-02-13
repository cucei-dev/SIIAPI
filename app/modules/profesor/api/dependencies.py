from app.modules.profesor.repositories.profesor_repository import ProfesorRepository
from app.modules.profesor.services.profesor_service import ProfesorService
from app.api.dependencies.database import get_session
from sqlmodel import Session
from fastapi import Depends

def get_user_service(
    session: Session = Depends(get_session),
) -> ProfesorService:
    return ProfesorService(
        repository=ProfesorRepository(session=session),
    )
