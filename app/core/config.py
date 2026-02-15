import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


def get_bool(value, default=False):
    if value is None:
        return default
    return str(value).lower() in ("true", "1", "yes")


def get_float(value, default=0.0):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


class Settings:
    DB_URL: str = os.getenv("DB_URL", "sqlite:///./db.sqlite3")

    APP_NAME: str = os.getenv("APP_NAME")
    APP_SITE: str = os.getenv("APP_SITE", "localhost")
    APP_ENV: str = os.getenv("APP_ENV", "dev")
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = os.getenv("APP_DESCRIPTION")
    APP_DEBUG: bool = get_bool(os.getenv("APP_DEBUG", "true"))
    
    # Database seeding - set to true to run seed data on startup (production)
    DB_SEED_ON_STARTUP: bool = get_bool(os.getenv("DB_SEED_ON_STARTUP", "false"))

    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key")
    DUMMY_HASH: str = os.getenv("DUMMY_HASH")
    ALGORITHM: str = "HS256"

    SIIAU_URL: str = os.getenv("SIIAU_URL")


settings = Settings()
