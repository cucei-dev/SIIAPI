from fastapi import FastAPI
from app.api import router as api_router
from app.core.config import settings
from app.core.database import init_db
from contextlib import asynccontextmanager
from app.core.seed import seed_data

@asynccontextmanager
async def lifespan(app: FastAPI):
    if settings.APP_DEBUG:
        init_db()
        await seed_data()
    yield


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=settings.APP_DESCRIPTION,
    lifespan=lifespan
)

app.include_router(api_router, prefix="/api")
