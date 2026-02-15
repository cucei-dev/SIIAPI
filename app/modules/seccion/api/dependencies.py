from fastapi import Depends
from sqlmodel import Session

from app.api.dependencies.database import get_session
from app.modules.calendario.repositories.calendario_repository import \
    CalendarioRepository
from app.modules.centro.repositories.centro_repository import \
    CentroUniversitarioRepository
from app.modules.materia.repositories.materia_repository import \
    MateriaRepository
from app.modules.profesor.repositories.profesor_repository import \
    ProfesorRepository
from app.modules.seccion.repositories.seccion_repository import \
    SeccionRepository
from app.modules.seccion.services.seccion_service import SeccionService


def get_seccion_service(
    session: Session = Depends(get_session),
) -> SeccionService:
    return SeccionService(
        repository=SeccionRepository(session=session),
        calendario_repository=CalendarioRepository(session=session),
        centro_repository=CentroUniversitarioRepository(session=session),
        materia_repository=MateriaRepository(session=session),
        profesor_repository=ProfesorRepository(session=session),
    )
