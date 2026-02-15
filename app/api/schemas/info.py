from pydantic import BaseModel

from app.core.config import settings


class Info(BaseModel):
    status: str = "ok"
    version: str = settings.APP_VERSION
    site: str = settings.APP_SITE
    name: str = settings.APP_NAME
    description: str = settings.APP_DESCRIPTION
    debug: bool = settings.APP_DEBUG
