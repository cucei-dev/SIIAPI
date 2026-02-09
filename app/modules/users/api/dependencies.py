from app.modules.users.repositories.user_repository import UserRepository
from app.modules.users.services.user_service import UserService
from app.api.dependencies.database import get_session
from sqlmodel import Session
from fastapi import Depends

def get_user_service(
    session: Session = Depends(get_session),
) -> UserService:
    return UserService(
        repository=UserRepository(session=session),
    )
