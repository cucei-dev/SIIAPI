from fastapi import APIRouter, Depends

from app.api.dependencies.auth import user_is_staff
from app.modules.tasks.services.task_service import TasksService
from app.modules.users.models import User

from .dependencies import get_tasks_service

router = APIRouter()


@router.get("/importar-secciones")
async def importar_secciones(
    calendario_id: int,
    centro_id: int,
    update: bool = False,
    service: TasksService = Depends(get_tasks_service),
    user: User = Depends(user_is_staff),
):
    return service.get_secciones(
        calendario_id=calendario_id,
        centro_id=centro_id,
        update_existing=update,
    )


@router.post("/importar-secciones-manual")
async def importar_secciones_manual(
    data: list[dict],
    calendario_id: int,
    centro_id: int,
    update: bool = False,
    service: TasksService = Depends(get_tasks_service),
    user: User = Depends(user_is_staff),
):
    return service.save_secciones(
        data=data,
        calendario_id=calendario_id,
        centro_id=centro_id,
        update_if_exists=update,
    )
