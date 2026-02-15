from fastapi import APIRouter, Depends, Query, status

from app.api.dependencies.auth import user_is_staff
from app.api.schemas import Pagination
from app.modules.seccion.schemas import (SeccionCreate, SeccionRead,
                                         SeccionUpdate)
from app.modules.seccion.services.seccion_service import SeccionService
from app.modules.users.models import User

from .dependencies import get_seccion_service

router = APIRouter()


@router.post("/", response_model=SeccionRead, status_code=status.HTTP_201_CREATED)
async def create_seccion(
    data: SeccionCreate,
    service: SeccionService = Depends(get_seccion_service),
    user: User = Depends(user_is_staff),
):
    return service.create_seccion(data)


@router.get("/{seccion_id}", response_model=SeccionRead)
async def get_seccion(
    seccion_id: int,
    service: SeccionService = Depends(get_seccion_service),
):
    return service.get_seccion(seccion_id)


@router.get("/", response_model=Pagination[SeccionRead])
async def list_secciones(
    nrc: str | None = None,
    centro_id: int | None = None,
    materia_id: int | None = None,
    profesor_id: int | None = None,
    calendario_id: int | None = None,
    search: str | None = None,
    skip: int = 0,
    limit: int = Query(default=100, ge=1, le=100),
    service: SeccionService = Depends(get_seccion_service),
):
    seccions, total = service.list_secciones(
        nrc=nrc,
        centro_id=centro_id,
        materia_id=materia_id,
        profesor_id=profesor_id,
        calendario_id=calendario_id,
        search=search,
        skip=skip,
        limit=limit,
    )
    return Pagination(
        total=total,
        results=seccions,
    )


@router.put("/{seccion_id}", response_model=SeccionRead)
async def update_seccion(
    seccion_id: int,
    data: SeccionUpdate,
    service: SeccionService = Depends(get_seccion_service),
    user: User = Depends(user_is_staff),
):
    return service.update_seccion(seccion_id, data)


@router.patch("/{seccion_id}", response_model=SeccionRead)
async def update_seccion_partial(
    seccion_id: int,
    data: SeccionUpdate,
    service: SeccionService = Depends(get_seccion_service),
    user: User = Depends(user_is_staff),
):
    return service.update_seccion(seccion_id, data)


@router.delete("/{seccion_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_seccion(
    seccion_id: int,
    service: SeccionService = Depends(get_seccion_service),
    user: User = Depends(user_is_staff),
):
    service.delete_seccion(seccion_id)
