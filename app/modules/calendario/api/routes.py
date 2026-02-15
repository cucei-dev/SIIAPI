from fastapi import APIRouter, Depends, Query, status

from app.api.dependencies.auth import user_is_staff
from app.api.schemas import Pagination
from app.modules.calendario.schemas import (CalendarioCreate, CalendarioRead,
                                            CalendarioUpdate)
from app.modules.calendario.services.calendario_service import \
    CalendarioService
from app.modules.users.models import User

from .dependencies import get_calendario_service

router = APIRouter()


@router.post("/", response_model=CalendarioRead, status_code=status.HTTP_201_CREATED)
async def create_calendario(
    data: CalendarioCreate,
    service: CalendarioService = Depends(get_calendario_service),
    user: User = Depends(user_is_staff),
):
    return service.create_calendario(data)


@router.get("/{calendario_id}", response_model=CalendarioRead)
async def get_calendario(
    calendario_id: int,
    service: CalendarioService = Depends(get_calendario_service),
):
    return service.get_calendario(calendario_id)


@router.get("/", response_model=Pagination[CalendarioRead])
async def list_calendarios(
    siiau_id: int | None = None,
    search: str | None = None,
    skip: int = 0,
    limit: int = Query(default=100, ge=1, le=100),
    service: CalendarioService = Depends(get_calendario_service),
):
    calendarios, total = service.list_calendarios(
        siiau_id=siiau_id,
        search=search,
        skip=skip,
        limit=limit,
    )
    return Pagination(
        total=total,
        results=calendarios,
    )


@router.put("/{calendario_id}", response_model=CalendarioRead)
async def update_calendario(
    calendario_id: int,
    data: CalendarioUpdate,
    service: CalendarioService = Depends(get_calendario_service),
    user: User = Depends(user_is_staff),
):
    return service.update_calendario(calendario_id, data)


@router.patch("/{calendario_id}", response_model=CalendarioRead)
async def update_calendario_partial(
    calendario_id: int,
    data: CalendarioUpdate,
    service: CalendarioService = Depends(get_calendario_service),
    user: User = Depends(user_is_staff),
):
    return service.update_calendario(calendario_id, data)


@router.delete("/{calendario_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_calendario(
    calendario_id: int,
    service: CalendarioService = Depends(get_calendario_service),
    user: User = Depends(user_is_staff),
):
    service.delete_calendario(calendario_id)
