from app.modules.centro.repositories.centro_repository import CentroUniversitarioRepository
from app.modules.centro.services.centro_service import CentroUniversitarioService
from app.api.dependencies.database import get_session
from sqlmodel import Session
from fastapi import Depends

def get_user_service(
    session: Session = Depends(get_session),
) -> CentroUniversitarioService:
    return CentroUniversitarioService(
        repository=CentroUniversitarioRepository(session=session),
    )
