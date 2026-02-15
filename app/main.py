from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api import router as api_router
from app.core.config import settings
from app.core.database import init_db
from app.core.migrations import run_migrations
from app.core.seed import seed_data
from app.api.schemas import Info

@asynccontextmanager
async def lifespan(app: FastAPI):
    if settings.APP_DEBUG:
        # In debug mode, use SQLModel's create_all for quick development
        init_db()
        seed_data()
    else:
        # In production, use Alembic migrations
        run_migrations()
        
        # Optionally seed data in production if DB_SEED_ON_STARTUP is True
        if settings.DB_SEED_ON_STARTUP:
            seed_data()
    yield


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=settings.APP_DESCRIPTION,
    lifespan=lifespan,
)

@app.get("/", response_model=Info)
async def get_info():
    return Info()

app.include_router(api_router, prefix="/api")
