from fastapi import APIRouter, Depends, status
from app.modules.materia.schemas import MateriaCreate, MateriaRead, MateriaUpdate
from app.modules.materia.services.materia_service import MateriaService
from .dependencies import get_materia_service
from app.api.schemas import Pagination
from app.api.dependencies.auth import user_is_staff
from app.modules.users.models import User

router = APIRouter()

@router.post("/", response_model=MateriaRead, status_code=status.HTTP_201_CREATED)
async def create_materia(
    data: MateriaCreate,
    service: MateriaService = Depends(get_materia_service),
    #user: User = Depends(user_is_staff),
):
        return await service.create_materia(data)

@router.get("/{materia_id}", response_model=MateriaRead)
async def get_materia(
    materia_id: int,
    service: MateriaService = Depends(get_materia_service),
    #user: User = Depends(user_is_staff),
):
    return service.get_materia(materia_id)

@router.get("/", response_model=Pagination[MateriaRead])
async def list_materias(
    search: str | None = None,
    skip: int = 0,
    limit: int = 100,
    service: MateriaService = Depends(get_materia_service),
    #user: User = Depends(user_is_staff),
):
    materias, total = service.list_materias(
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
    service: MateriaService = Depends(get_materia_service),
    #user: User = Depends(user_is_staff),
):
    return service.update_materia(materia_id, data)

@router.patch("/{materia_id}", response_model=MateriaRead)
async def update_materia_partial(
    materia_id: int,
    data: MateriaUpdate,
    service: MateriaService = Depends(get_materia_service),
    #user: User = Depends(user_is_staff),
):
    return service.update_materia(materia_id, data)

@router.delete("/{materia_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_materia(
    materia_id: int,
    service: MateriaService = Depends(get_materia_service),
    #user: User = Depends(user_is_staff),
):
    service.delete_materia(materia_id)
