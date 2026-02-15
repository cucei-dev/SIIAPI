from fastapi import APIRouter, Depends
from app.api.dependencies.auth import user_is_staff
from app.modules.users.models import User
from .dependencies import get_tasks_service
from app.modules.tasks.services.task_service import TasksService

router = APIRouter()

@router.get("/importar-secciones")
async def importar_secciones(
    calendario_id: int,
    centro_id: int,
    service: TasksService = Depends(get_tasks_service),
    user: User = Depends(user_is_staff),
):
    return service.get_secciones(
        calendario_id=calendario_id,
        centro_id=centro_id,
    )
