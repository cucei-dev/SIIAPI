from app.modules.edificio.repositories.edificio_repository import EdificioRepository
from app.modules.edificio.services.edificio_service import EdificioService
from app.api.dependencies.database import get_session
from sqlmodel import Session
from fastapi import Depends

def get_user_service(
    session: Session = Depends(get_session),
) -> EdificioService:
    return EdificioService(
        repository=EdificioRepository(session=session),
    )
