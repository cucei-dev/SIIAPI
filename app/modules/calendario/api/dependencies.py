from app.modules.calendario.repositories.calendario_repository import CalendarioRepository
from app.modules.calendario.services.calendario_service import CalendarioService
from app.api.dependencies.database import get_session
from sqlmodel import Session
from fastapi import Depends

def get_user_service(
    session: Session = Depends(get_session),
) -> CalendarioService:
    return CalendarioService(
        repository=CalendarioRepository(session=session),
    )
