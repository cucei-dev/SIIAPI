from fastapi import Depends
from sqlmodel import Session

from app.api.dependencies.database import get_session
from app.modules.centro.repositories.centro_repository import \
    CentroUniversitarioRepository
from app.modules.edificio.repositories.edificio_repository import \
    EdificioRepository
from app.modules.edificio.services.edificio_service import EdificioService


def get_edificio_service(
    session: Session = Depends(get_session),
) -> EdificioService:
    return EdificioService(
        repository=EdificioRepository(session=session),
        centro_repository=CentroUniversitarioRepository(session=session),
    )
