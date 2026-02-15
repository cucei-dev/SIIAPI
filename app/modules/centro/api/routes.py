from fastapi import APIRouter, Depends, status
from app.modules.centro.schemas import CentroUniversitarioCreate, CentroUniversitarioRead, CentroUniversitarioUpdate
from app.modules.centro.services.centro_service import CentroUniversitarioService
from .dependencies import get_centro_service
from app.api.schemas import Pagination
from app.api.dependencies.auth import user_is_staff
from app.modules.users.models import User

router = APIRouter()

@router.post("/", response_model=CentroUniversitarioRead, status_code=status.HTTP_201_CREATED)
async def create_centro(
    data: CentroUniversitarioCreate,
    service: CentroUniversitarioService = Depends(get_centro_service),
    user: User = Depends(user_is_staff),
):
        return service.create_centro(data)

@router.get("/{centro_id}", response_model=CentroUniversitarioRead)
async def get_centro(
    centro_id: int,
    service: CentroUniversitarioService = Depends(get_centro_service),
    user: User = Depends(user_is_staff),
):
    return service.get_centro(centro_id)

@router.get("/", response_model=Pagination[CentroUniversitarioRead])
async def list_centros(
    siiau_id: int | None = None,
    search: str | None = None,
    skip: int = 0,
    limit: int = 100,
    service: CentroUniversitarioService = Depends(get_centro_service),
    user: User = Depends(user_is_staff),
):
    centros, total = service.list_centros(
        siiau_id=siiau_id,
        search=search,
        skip=skip,
        limit=limit,
    )
    return Pagination(
        total=total,
        results=centros,
    )

@router.put("/{centro_id}", response_model=CentroUniversitarioRead)
async def update_centro(
    centro_id: int,
    data: CentroUniversitarioUpdate,
    service: CentroUniversitarioService = Depends(get_centro_service),
    user: User = Depends(user_is_staff),
):
    return service.update_centro(centro_id, data)

@router.patch("/{centro_id}", response_model=CentroUniversitarioRead)
async def update_centro_partial(
    centro_id: int,
    data: CentroUniversitarioUpdate,
    service: CentroUniversitarioService = Depends(get_centro_service),
    user: User = Depends(user_is_staff),
):
    return service.update_centro(centro_id, data)

@router.delete("/{centro_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_centro(
    centro_id: int,
    service: CentroUniversitarioService = Depends(get_centro_service),
    user: User = Depends(user_is_staff),
):
    service.delete_centro(centro_id)
