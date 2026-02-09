from fastapi import APIRouter, Depends, status
from app.modules.users.schemas import UserRead, UserCreate, UserUpdate
from app.modules.users.services.user_service import UserService
from .dependencies import get_user_service
from app.api.schemas import Pagination
from app.api.dependencies.auth import user_is_superuser
from app.modules.users.models import User

router = APIRouter()

@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(
    data: UserCreate,
    service: UserService = Depends(get_user_service),
    user: User = Depends(user_is_superuser),
):
        return await service.create_user(data)

@router.get("/{user_id}", response_model=UserRead)
async def get_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
    user: User = Depends(user_is_superuser),
):
    return service.get_user(user_id)

@router.get("/", response_model=Pagination[UserRead])
async def list_users(
    email: str | None = None,
    is_active: bool | None = None,
    is_superuser: bool | None = None,
    is_staff: bool | None = None,
    search: str | None = None,
    skip: int = 0,
    limit: int = 100,
    service: UserService = Depends(get_user_service),
    user: User = Depends(user_is_superuser),
):
    users, total = service.list_users(
        email=email,
        is_active=is_active,
        is_superuser=is_superuser,
        is_staff=is_staff,
        search=search,
        skip=skip,
        limit=limit,
    )
    return Pagination(
        total=total,
        results=users,
    )

@router.put("/{user_id}", response_model=UserRead)
async def update_user(
    user_id: int,
    data: UserUpdate,
    service: UserService = Depends(get_user_service),
    user: User = Depends(user_is_superuser),
):
    return service.update_user(user_id, data)

@router.patch("/{user_id}", response_model=UserRead)
async def update_user_partial(
    user_id: int,
    data: UserUpdate,
    service: UserService = Depends(get_user_service),
    user: User = Depends(user_is_superuser),
):
    return service.update_user(user_id, data)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def soft_delete_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
    user: User = Depends(user_is_superuser),
):
    service.delete_user(user_id)

@router.delete("/{user_id}/hard", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
    user: User = Depends(user_is_superuser),
):
    service.hard_delete_user(user_id)
