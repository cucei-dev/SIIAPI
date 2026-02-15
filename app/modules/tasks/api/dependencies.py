from app.modules.tasks.services.task_service import TasksService
from fastapi import Depends
from app.modules.centro.services.centro_service import CentroUniversitarioService
from app.modules.centro.api.dependencies import get_centro_service
from app.modules.calendario.services.calendario_service import CalendarioService
from app.modules.calendario.api.dependencies import get_calendario_service
from app.modules.materia.services.materia_service import MateriaService
from app.modules.materia.api.dependencies import get_materia_service
from app.modules.profesor.services.profesor_service import ProfesorService
from app.modules.profesor.api.dependencies import get_profesor_service
from app.modules.edificio.services.edificio_service import EdificioService
from app.modules.edificio.api.dependencies import get_edificio_service
from app.modules.seccion.services.seccion_service import SeccionService
from app.modules.seccion.api.dependencies import get_seccion_service
from app.modules.aula.services.aula_service import AulaService
from app.modules.aula.api.dependencies import get_aula_service
from app.modules.clase.services.clase_service import ClaseService
from app.modules.clase.api.dependencies import get_clase_service
from app.modules.tasks.schemas.siiau import SeccionSiiau

def get_tasks_service(
    centro_service: CentroUniversitarioService = Depends(get_centro_service),
    calendario_service: CalendarioService = Depends(get_calendario_service),
    materia_service: MateriaService = Depends(get_materia_service),
    profesor_service: ProfesorService = Depends(get_profesor_service),
    edificio_service: EdificioService = Depends(get_edificio_service),
    seccion_service: SeccionService = Depends(get_seccion_service),
    aula_service: AulaService = Depends(get_aula_service),
    clase_service: ClaseService = Depends(get_clase_service),
) -> TasksService:
    return TasksService(
        centro_service=centro_service,
        calendario_service=calendario_service,
        materia_service=materia_service,
        profesor_service=profesor_service,
        edificio_service=edificio_service,
        seccion_service=seccion_service,
        aula_service=aula_service,
        clase_service=clase_service,
    )
