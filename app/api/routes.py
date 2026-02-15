from fastapi import APIRouter

from app.modules.aula.api.routes import router as aulas_router
from app.modules.auth.api.routes import router as auth_router
from app.modules.calendario.api.routes import router as calendarios_router
from app.modules.centro.api.routes import router as centros_router
from app.modules.clase.api.routes import router as clases_router
from app.modules.edificio.api.routes import router as edificios_router
from app.modules.materia.api.routes import router as materias_router
from app.modules.profesor.api.routes import router as profesores_router
from app.modules.seccion.api.routes import router as secciones_router
from app.modules.tasks.api.routes import router as tasks_router
from app.modules.users.api.routes import router as users_router

router = APIRouter()

router.include_router(calendarios_router, prefix="/calendarios", tags=["Calendarios"])
router.include_router(
    centros_router, prefix="/centros", tags=["Centros Universitarios"]
)
router.include_router(materias_router, prefix="/materias", tags=["Materias"])
router.include_router(secciones_router, prefix="/secciones", tags=["Secciones"])
router.include_router(profesores_router, prefix="/profesores", tags=["Profesores"])
router.include_router(clases_router, prefix="/clases", tags=["Clases"])
router.include_router(edificios_router, prefix="/edificios", tags=["Edificios"])
router.include_router(aulas_router, prefix="/aulas", tags=["Aulas"])
router.include_router(auth_router, prefix="/auth", tags=["Auth"])
router.include_router(users_router, prefix="/users", tags=["Users"])
router.include_router(tasks_router, prefix="/tasks", tags=["Tasks"])
