from fastapi import APIRouter, Depends, status
from app.modules.profesor.schemas import ProfesorCreate, ProfesorRead, ProfesorUpdate
from app.modules.profesor.services.profesor_service import ProfesorService
from .dependencies import get_profesor_service
from app.api.schemas import Pagination
from app.api.dependencies.auth import user_is_staff
from app.modules.users.models import User

router = APIRouter()

@router.post("/", response_model=ProfesorRead, status_code=status.HTTP_201_CREATED)
async def create_profesor(
    data: ProfesorCreate,
    service: ProfesorService = Depends(get_profesor_service),
    user: User = Depends(user_is_staff),
):
        return service.create_profesor(data)

@router.get("/{profesor_id}", response_model=ProfesorRead)
async def get_profesor(
    profesor_id: int,
    service: ProfesorService = Depends(get_profesor_service),
    user: User = Depends(user_is_staff),
):
    return service.get_profesor(profesor_id)

@router.get("/", response_model=Pagination[ProfesorRead])
async def list_profesores(
    name: str | None = None,
    search: str | None = None,
    skip: int = 0,
    limit: int = 100,
    service: ProfesorService = Depends(get_profesor_service),
    user: User = Depends(user_is_staff),
):
    profesors, total = service.list_profesores(
        name=name,
        search=search,
        skip=skip,
        limit=limit,
    )
    return Pagination(
        total=total,
        results=profesors,
    )

@router.put("/{profesor_id}", response_model=ProfesorRead)
async def update_profesor(
    profesor_id: int,
    data: ProfesorUpdate,
    service: ProfesorService = Depends(get_profesor_service),
    user: User = Depends(user_is_staff),
):
    return service.update_profesor(profesor_id, data)

@router.patch("/{profesor_id}", response_model=ProfesorRead)
async def update_profesor_partial(
    profesor_id: int,
    data: ProfesorUpdate,
    service: ProfesorService = Depends(get_profesor_service),
    user: User = Depends(user_is_staff),
):
    return service.update_profesor(profesor_id, data)

@router.delete("/{profesor_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_profesor(
    profesor_id: int,
    service: ProfesorService = Depends(get_profesor_service),
    user: User = Depends(user_is_staff),
):
    service.delete_profesor(profesor_id)
