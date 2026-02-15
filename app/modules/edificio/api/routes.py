from fastapi import APIRouter, Depends, status

from app.api.dependencies.auth import user_is_staff
from app.api.schemas import Pagination
from app.modules.edificio.schemas import (EdificioCreate, EdificioRead,
                                          EdificioUpdate)
from app.modules.edificio.services.edificio_service import EdificioService
from app.modules.users.models import User

from .dependencies import get_edificio_service

router = APIRouter()


@router.post("/", response_model=EdificioRead, status_code=status.HTTP_201_CREATED)
async def create_edificio(
    data: EdificioCreate,
    service: EdificioService = Depends(get_edificio_service),
    user: User = Depends(user_is_staff),
):
    return service.create_edificio(data)


@router.get("/{edificio_id}", response_model=EdificioRead)
async def get_edificio(
    edificio_id: int,
    service: EdificioService = Depends(get_edificio_service),
    user: User = Depends(user_is_staff),
):
    return service.get_edificio(edificio_id)


@router.get("/", response_model=Pagination[EdificioRead])
async def list_edificios(
    centro_id: int | None = None,
    name: str | None = None,
    search: str | None = None,
    skip: int = 0,
    limit: int = 100,
    service: EdificioService = Depends(get_edificio_service),
    user: User = Depends(user_is_staff),
):
    edificios, total = service.list_edificios(
        centro_id=centro_id,
        name=name,
        search=search,
        skip=skip,
        limit=limit,
    )
    return Pagination(
        total=total,
        results=edificios,
    )


@router.put("/{edificio_id}", response_model=EdificioRead)
async def update_edificio(
    edificio_id: int,
    data: EdificioUpdate,
    service: EdificioService = Depends(get_edificio_service),
    user: User = Depends(user_is_staff),
):
    return service.update_edificio(edificio_id, data)


@router.patch("/{edificio_id}", response_model=EdificioRead)
async def update_edificio_partial(
    edificio_id: int,
    data: EdificioUpdate,
    service: EdificioService = Depends(get_edificio_service),
    user: User = Depends(user_is_staff),
):
    return service.update_edificio(edificio_id, data)


@router.delete("/{edificio_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_edificio(
    edificio_id: int,
    service: EdificioService = Depends(get_edificio_service),
    user: User = Depends(user_is_staff),
):
    service.delete_edificio(edificio_id)
