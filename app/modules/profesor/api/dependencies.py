from fastapi import Depends
from sqlmodel import Session

from app.api.dependencies.database import get_session
from app.modules.profesor.repositories.profesor_repository import \
    ProfesorRepository
from app.modules.profesor.services.profesor_service import ProfesorService


def get_profesor_service(
    session: Session = Depends(get_session),
) -> ProfesorService:
    return ProfesorService(
        repository=ProfesorRepository(session=session),
    )
