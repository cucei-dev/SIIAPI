from fastapi import Depends
from sqlmodel import Session

from app.api.dependencies.database import get_session
from app.modules.calendario.repositories.calendario_repository import \
    CalendarioRepository
from app.modules.calendario.services.calendario_service import \
    CalendarioService


def get_calendario_service(
    session: Session = Depends(get_session),
) -> CalendarioService:
    return CalendarioService(
        repository=CalendarioRepository(session=session),
    )
