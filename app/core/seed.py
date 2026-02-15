from app.api.dependencies.database import get_session
from app.modules.users.api.dependencies import get_user_service
from app.modules.users.schemas import UserCreate


def seed_data():
    session = next(get_session())
    create_superuser(session)


def create_superuser(session):
    service = get_user_service(session)
    _, total = service.list_users()

    if not total:
        service.create_user(
            UserCreate(
                name="Admin",
                email="admin@example.com",
                password="admin",
                is_active=True,
                is_superuser=True,
                credits=100,
            )
        )
