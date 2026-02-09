from sqlmodel import SQLModel, create_engine
from app.core.config import settings

connect_args = {}
if settings.DB_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(
    settings.DB_URL,
    connect_args=connect_args,
    echo=settings.APP_DEBUG
)

def init_db():
     import app.modules.users.models
     import app.modules.auth.models

     SQLModel.metadata.create_all(engine)
