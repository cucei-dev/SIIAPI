from app.modules.clase.repositories.clase_repository import ClaseRepository
from app.modules.clase.schemas import ClaseCreate, ClaseUpdate
from app.modules.clase.models import Clase
from app.core.exceptions import NotFoundException, ConflictException

class ClaseService:
    def __init__(
        self,
        repository: ClaseRepository,
    ):
        self.repository = repository

    def create_clase(self, data: ClaseCreate) -> Clase:
        clase = Clase.model_validate(data)
        return self.repository.create(clase)

    def get_clase(self, clase_id: int):
        clase = self.repository.get(clase_id)
        if not clase:
            raise NotFoundException("Clase not found.")

    def list_clases(self, **filters) -> tuple[list[Clase], int]:
        return self.repository.list(filters)

    def update_clase(self, clase_id: int, data: ClaseUpdate) -> Clase:
        clase = self.repository.get(clase_id)
        if not clase:
            raise NotFoundException("Clase not found.")

        update_data = data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            if value is not None:
                setattr(clase, key, value)

        return self.repository.update(clase)

    def delete_clase(self, clase_id) -> None:
        clase = self.repository.get(clase_id)
        if not clase:
            raise NotFoundException("Clase not found.")

        return self.repository.delete(clase)
