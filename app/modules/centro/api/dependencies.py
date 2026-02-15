from fastapi import Depends
from sqlmodel import Session

from app.api.dependencies.database import get_session
from app.modules.centro.repositories.centro_repository import \
    CentroUniversitarioRepository
from app.modules.centro.services.centro_service import \
    CentroUniversitarioService


def get_centro_service(
    session: Session = Depends(get_session),
) -> CentroUniversitarioService:
    return CentroUniversitarioService(
        repository=CentroUniversitarioRepository(session=session),
    )
