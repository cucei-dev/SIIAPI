from app.modules.users.api.dependencies import get_user_service
from app.modules.users.schemas import UserCreate
from app.api.dependencies.database import get_session

async def seed_data():
    session = next(get_session())
    await create_superuser(session)

async def create_superuser(session):
    service = get_user_service(session)
    _,total = service.list_users()

    if not total:
        await service.create_user(
            UserCreate(
                name="Admin",
                email="admin@example.com",
                password="admin",
                is_active=True,
                is_superuser=True,
                credits=100,
            )
        )
