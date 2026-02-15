from app.core.exceptions import ConflictException, NotFoundException
from app.modules.profesor.models import Profesor
from app.modules.profesor.repositories.profesor_repository import \
    ProfesorRepository
from app.modules.profesor.schemas import ProfesorCreate, ProfesorUpdate


class ProfesorService:
    def __init__(
        self,
        repository: ProfesorRepository,
    ):
        self.repository = repository

    def create_profesor(self, data: ProfesorCreate) -> Profesor:
        profesor = Profesor.model_validate(data)
        _, total = self.repository.list({"name": profesor.name})

        if total != 0:
            raise ConflictException("Profesor with that name already exists.")

        return self.repository.create(profesor)

    def get_profesor(self, profesor_id: int) -> Profesor:
        profesor = self.repository.get(profesor_id)
        if not profesor:
            raise NotFoundException("Profesor not found.")

        return profesor

    def list_profesores(self, **filters) -> tuple[list[Profesor], int]:
        return self.repository.list(filters)

    def update_profesor(self, profesor_id: int, data: ProfesorUpdate) -> Profesor:
        profesor = self.repository.get(profesor_id)
        if not profesor:
            raise NotFoundException("Profesor not found.")

        update_data = data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            if value is not None:
                setattr(profesor, key, value)

        return self.repository.update(profesor)

    def delete_profesor(self, profesor_id) -> None:
        profesor = self.repository.get(profesor_id)
        if not profesor:
            raise NotFoundException("Profesor not found.")

        return self.repository.delete(profesor)
