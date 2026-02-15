from app.core.exceptions import ConflictException, NotFoundException
from app.modules.centro.repositories.centro_repository import \
    CentroUniversitarioRepository
from app.modules.edificio.models import Edificio
from app.modules.edificio.repositories.edificio_repository import \
    EdificioRepository
from app.modules.edificio.schemas import EdificioCreate, EdificioUpdate


class EdificioService:
    def __init__(
        self,
        repository: EdificioRepository,
        centro_repository: CentroUniversitarioRepository,
    ):
        self.repository = repository
        self.centro_repository = centro_repository

    def create_edificio(self, data: EdificioCreate) -> Edificio:
        edificio = Edificio.model_validate(data)
        centro = self.centro_repository.get(edificio.centro_id)

        if not centro:
            raise NotFoundException("Centro Universitario not found.")

        _, total = self.repository.list(
            {"centro_id": edificio.centro_id, "name": edificio.name}
        )

        if total != 0:
            raise ConflictException(
                "Edificio with that name in that Centro Universitario already exists."
            )

        return self.repository.create(edificio)

    def get_edificio(self, edificio_id: int) -> Edificio:
        edificio = self.repository.get(edificio_id)
        if not edificio:
            raise NotFoundException("Edificio not found.")

        return edificio

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
