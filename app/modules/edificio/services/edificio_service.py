from app.modules.edificio.repositories.edificio_repository import EdificioRepository
from app.modules.edificio.schemas import EdificioCreate, EdificioUpdate
from app.modules.edificio.models import Edificio
from app.core.exceptions import NotFoundException, ConflictException

class EdificioService:
    def __init__(
        self,
        repository: EdificioRepository,
    ):
        self.repository = repository

    def create_edificio(self, data: EdificioCreate) -> Edificio:
        edificio = Edificio.model_validate(data)
        return self.repository.create(edificio)

    def get_edificio(self, edificio_id: int):
        edificio = self.repository.get(edificio_id)
        if not edificio:
            raise NotFoundException("Edificio not found.")

    def list_edificios(self, **filters) -> tuple[list[Edificio], int]:
        return self.repository.list(filters)

    def update_edificio(self, edificio_id: int, data: EdificioUpdate) -> Edificio:
        edificio = self.repository.get(edificio_id)
        if not edificio:
            raise NotFoundException("Edificio not found.")

        update_data = data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            if value is not None:
                setattr(edificio, key, value)

        return self.repository.update(edificio)

    def delete_edificio(self, edificio_id) -> None:
        edificio = self.repository.get(edificio_id)
        if not edificio:
            raise NotFoundException("Edificio not found.")

        return self.repository.delete(edificio)
