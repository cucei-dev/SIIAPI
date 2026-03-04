from typing import Annotated

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
    service: Annotated[TasksService, Depends(get_tasks_service)],
    user: Annotated[User, Depends(user_is_staff)],
):
    return service.get_secciones(
        calendario_id=calendario_id,
        centro_id=centro_id,
    )


@router.get("/actualizar-secciones")
async def actualizar_secciones(
    calendario_id: int,
    centro_id: int,
    service: Annotated[TasksService, Depends(get_tasks_service)],
    user: Annotated[User, Depends(user_is_staff)],
    full_update: bool = False,
):
    return service.update_all_secciones(
        calendario_id=calendario_id,
        centro_id=centro_id,
    )


@router.post("/importar-secciones-manual")
async def importar_secciones_manual(
    data: list[dict],
    calendario_id: int,
    centro_id: int,
    service: Annotated[TasksService, Depends(get_tasks_service)],
    user: Annotated[User, Depends(user_is_staff)],
    update: bool = False,
    full_update: bool = False,
):
    return service.save_secciones(
        data=data,
        calendario_id=calendario_id,
        centro_id=centro_id,
        update_if_exists=update,
        full_update=full_update,
    )
