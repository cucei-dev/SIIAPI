from app.modules.clase.repositories.clase_repository import ClaseRepository
from app.modules.clase.services.clase_service import ClaseService
from app.api.dependencies.database import get_session
from sqlmodel import Session
from fastapi import Depends

def get_user_service(
    session: Session = Depends(get_session),
) -> ClaseService:
    return ClaseService(
        repository=ClaseRepository(session=session),
    )
