from app.modules.materia.repositories.materia_repository import MateriaRepository
from app.modules.materia.schemas import MateriaCreate, MateriaUpdate
from app.modules.materia.models import Materia
from app.core.exceptions import NotFoundException, ConflictException

class MateriaService:
    def __init__(
        self,
        repository: MateriaRepository,
    ):
        self.repository = repository

    def create_materia(self, data: MateriaCreate) -> Materia:
        materia = Materia.model_validate(data)
        _,total = self.repository.list({"clave": materia.clave})

        if total != 0:
            raise ConflictException("Materia with that clave already exists.")

        return self.repository.create(materia)

    def get_materia(self, materia_id: int):
        materia = self.repository.get(materia_id)
        if not materia:
            raise NotFoundException("Materia not found.")

    def list_materias(self, **filters) -> tuple[list[Materia], int]:
        return self.repository.list(filters)

    def update_materia(self, materia_id: int, data: MateriaUpdate) -> Materia:
        materia = self.repository.get(materia_id)
        if not materia:
            raise NotFoundException("Materia not found.")

        update_data = data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            if value is not None:
                setattr(materia, key, value)

        return self.repository.update(materia)

    def delete_materia(self, materia_id) -> None:
        materia = self.repository.get(materia_id)
        if not materia:
            raise NotFoundException("Materia not found.")

        return self.repository.delete(materia)
