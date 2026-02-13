from app.modules.seccion.repositories.seccion_repository import SeccionRepository
from app.modules.seccion.services.seccion_service import SeccionService
from app.api.dependencies.database import get_session
from sqlmodel import Session
from fastapi import Depends

def get_seccion_service(
    session: Session = Depends(get_session),
) -> SeccionService:
    return SeccionService(
        repository=SeccionRepository(session=session),
    )
