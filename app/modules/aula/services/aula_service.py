from app.modules.aula.repositories.aula_repository import AulaRepository
from app.modules.aula.schemas import AulaCreate, AulaUpdate
from app.modules.aula.models import Aula
from app.core.exceptions import NotFoundException, ConflictException

class AulaService:
    def __init__(
        self,
        repository: AulaRepository,
    ):
        self.repository = repository

    def create_aula(self, data: AulaCreate) -> Aula:
        aula = Aula.model_validate(data)
        return self.repository.create(aula)

    def get_aula(self, aula_id: int):
        aula = self.repository.get(aula_id)
        if not aula:
            raise NotFoundException("Aula not found.")

    def list_aulas(self, **filters) -> tuple[list[Aula], int]:
        return self.repository.list(filters)

    def update_aula(self, aula_id: int, data: AulaUpdate) -> Aula:
        aula = self.repository.get(aula_id)
        if not aula:
            raise NotFoundException("Aula not found.")

        update_data = data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            if value is not None:
                setattr(aula, key, value)

        return self.repository.update(aula)

    def delete_aula(self, aula_id) -> None:
        aula = self.repository.get(aula_id)
        if not aula:
            raise NotFoundException("Aula not found.")

        return self.repository.delete(aula)
