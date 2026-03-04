from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from app.api.dependencies.auth import user_is_staff
from app.api.schemas import Pagination
from app.modules.materia.schemas import (MateriaCreate, MateriaRead,
                                         MateriaUpdate)
from app.modules.materia.services.materia_service import MateriaService
from app.modules.users.models import User

from .dependencies import get_materia_service

router = APIRouter()


@router.post("/", response_model=MateriaRead, status_code=status.HTTP_201_CREATED)
async def create_materia(
    data: MateriaCreate,
    service: Annotated[MateriaService, Depends(get_materia_service)],
    user: Annotated[User, Depends(user_is_staff)],
):
    return service.create_materia(data)


@router.get("/{materia_id}", response_model=MateriaRead)
async def get_materia(
    materia_id: int,
    service: Annotated[MateriaService, Depends(get_materia_service)],
):
    return service.get_materia(materia_id)


@router.get("/", response_model=Pagination[MateriaRead])
async def list_materias(
    service: Annotated[MateriaService, Depends(get_materia_service)],
    clave: str | None = None,
    search: str | None = None,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=100),
):
    materias, total = service.list_materias(
        clave=clave,
        search=search,
        skip=skip,
        limit=limit,
    )
    return Pagination(
        total=total,
        results=materias,
    )


@router.put("/{materia_id}", response_model=MateriaRead)
async def update_materia(
    materia_id: int,
    data: MateriaUpdate,
    service: Annotated[MateriaService, Depends(get_materia_service)],
    user: Annotated[User, Depends(user_is_staff)],
):
    return service.update_materia(materia_id, data)


@router.patch("/{materia_id}", response_model=MateriaRead)
async def update_materia_partial(
    materia_id: int,
    data: MateriaUpdate,
    service: Annotated[MateriaService, Depends(get_materia_service)],
    user: Annotated[User, Depends(user_is_staff)],
):
    return service.update_materia(materia_id, data)


@router.delete("/{materia_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_materia(
    materia_id: int,
    service: Annotated[MateriaService, Depends(get_materia_service)],
    user: Annotated[User, Depends(user_is_staff)],
):
    service.delete_materia(materia_id)
