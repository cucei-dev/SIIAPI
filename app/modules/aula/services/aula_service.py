from app.core.exceptions import ConflictException, NotFoundException
from app.modules.aula.models import Aula
from app.modules.aula.repositories.aula_repository import AulaRepository
from app.modules.aula.schemas import AulaCreate, AulaUpdate
from app.modules.edificio.repositories.edificio_repository import \
    EdificioRepository


class AulaService:
    def __init__(
        self,
        repository: AulaRepository,
        edificio_repository: EdificioRepository,
    ):
        self.repository = repository
        self.edificio_repository = edificio_repository

    def create_aula(self, data: AulaCreate) -> Aula:
        aula = Aula.model_validate(data)
        edificio = self.edificio_repository.get(aula.edificio_id)

        if not edificio:
            raise NotFoundException("Edificio not found.")

        _, total = self.repository.list(
            {"edificio_id": aula.edificio_id, "name": aula.name}
        )

        if total != 0:
            raise ConflictException(
                "Aula with that name in that Edificio already exists."
            )

        return self.repository.create(aula)

    def get_aula(self, aula_id: int) -> Aula:
        aula = self.repository.get(aula_id)
        if not aula:
            raise NotFoundException("Aula not found.")

        return aula

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
