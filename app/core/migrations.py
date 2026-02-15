"""
Alembic migration utilities for running migrations programmatically.
"""

import logging

from alembic import command
from alembic.config import Config

logger = logging.getLogger(__name__)


def run_migrations():
    """
    Run all pending Alembic migrations to upgrade the database to the latest version.
    This is used in production when APP_DEBUG is False.
    """
    try:
        logger.info("Running database migrations...")
        alembic_cfg = Config("alembic.ini")
        command.upgrade(alembic_cfg, "head")
        logger.info("Database migrations completed successfully")
    except Exception as e:
        logger.error(f"Error running migrations: {e}")
        raise
