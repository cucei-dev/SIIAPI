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
     import app.modules.centro.models
     import app.modules.materia.models
     import app.modules.seccion.models
     import app.modules.clase.models
     import app.modules.profesor.models
     import app.modules.aula.models
     import app.modules.edificio.models

     SQLModel.metadata.create_all(engine)
