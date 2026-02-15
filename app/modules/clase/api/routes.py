from datetime import time

from fastapi import APIRouter, Depends, status

from app.api.dependencies.auth import user_is_staff
from app.api.schemas import Pagination
from app.modules.clase.schemas import ClaseCreate, ClaseRead, ClaseUpdate
from app.modules.clase.services.clase_service import ClaseService
from app.modules.users.models import User

from .dependencies import get_clase_service

router = APIRouter()


@router.post("/", response_model=ClaseRead, status_code=status.HTTP_201_CREATED)
async def create_clase(
    data: ClaseCreate,
    service: ClaseService = Depends(get_clase_service),
    user: User = Depends(user_is_staff),
):
    return service.create_clase(data)


@router.get("/{clase_id}", response_model=ClaseRead)
async def get_clase(
    clase_id: int,
    service: ClaseService = Depends(get_clase_service),
):
    return service.get_clase(clase_id)


@router.get("/", response_model=Pagination[ClaseRead])
async def list_clases(
    seccion_id: int | None = None,
    aula_id: int | None = None,
    hora_inicio: time | None = None,
    hora_fin: time | None = None,
    dia: int | None = None,
    search: str | None = None,
    skip: int = 0,
    limit: int = 100,
    service: ClaseService = Depends(get_clase_service),
):
    clases, total = service.list_clases(
        seccion_id=seccion_id,
        aula_id=aula_id,
        hora_inicio=hora_inicio,
        hora_fin=hora_fin,
        dia=dia,
        search=search,
        skip=skip,
        limit=limit,
    )
    return Pagination(
        total=total,
        results=clases,
    )


@router.put("/{clase_id}", response_model=ClaseRead)
async def update_clase(
    clase_id: int,
    data: ClaseUpdate,
    service: ClaseService = Depends(get_clase_service),
    user: User = Depends(user_is_staff),
):
    return service.update_clase(clase_id, data)


@router.patch("/{clase_id}", response_model=ClaseRead)
async def update_clase_partial(
    clase_id: int,
    data: ClaseUpdate,
    service: ClaseService = Depends(get_clase_service),
    user: User = Depends(user_is_staff),
):
    return service.update_clase(clase_id, data)


@router.delete("/{clase_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_clase(
    clase_id: int,
    service: ClaseService = Depends(get_clase_service),
    user: User = Depends(user_is_staff),
):
    service.delete_clase(clase_id)
