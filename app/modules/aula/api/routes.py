from fastapi import APIRouter, Depends, status
from app.modules.aula.schemas import AulaCreate, AulaRead, AulaUpdate
from app.modules.aula.services.aula_service import AulaService
from .dependencies import get_aula_service
from app.api.schemas import Pagination
from app.api.dependencies.auth import user_is_staff
from app.modules.users.models import User

router = APIRouter()

@router.post("/", response_model=AulaRead, status_code=status.HTTP_201_CREATED)
async def create_aula(
    data: AulaCreate,
    service: AulaService = Depends(get_aula_service),
    user: User = Depends(user_is_staff),
):
        return service.create_aula(data)

@router.get("/{aula_id}", response_model=AulaRead)
async def get_aula(
    aula_id: int,
    service: AulaService = Depends(get_aula_service),
    user: User = Depends(user_is_staff),
):
    return service.get_aula(aula_id)

@router.get("/", response_model=Pagination[AulaRead])
async def list_aulas(
    edificio_id: int | None = None,
    name: str | None = None,
    search: str | None = None,
    skip: int = 0,
    limit: int = 100,
    service: AulaService = Depends(get_aula_service),
    user: User = Depends(user_is_staff),
):
    aulas, total = service.list_aulas(
        edificio_id=edificio_id,
        name=name,
        search=search,
        skip=skip,
        limit=limit,
    )
    return Pagination(
        total=total,
        results=aulas,
    )

@router.put("/{aula_id}", response_model=AulaRead)
async def update_aula(
    aula_id: int,
    data: AulaUpdate,
    service: AulaService = Depends(get_aula_service),
    user: User = Depends(user_is_staff),
):
    return service.update_aula(aula_id, data)

@router.patch("/{aula_id}", response_model=AulaRead)
async def update_aula_partial(
    aula_id: int,
    data: AulaUpdate,
    service: AulaService = Depends(get_aula_service),
    user: User = Depends(user_is_staff),
):
    return service.update_aula(aula_id, data)

@router.delete("/{aula_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_aula(
    aula_id: int,
    service: AulaService = Depends(get_aula_service),
    user: User = Depends(user_is_staff),
):
    service.delete_aula(aula_id)
