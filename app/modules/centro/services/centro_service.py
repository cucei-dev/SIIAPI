from app.core.exceptions import ConflictException, NotFoundException
from app.modules.centro.models import CentroUniversitario
from app.modules.centro.repositories.centro_repository import \
    CentroUniversitarioRepository
from app.modules.centro.schemas import (CentroUniversitarioCreate,
                                        CentroUniversitarioUpdate)


class CentroUniversitarioService:
    def __init__(
        self,
        repository: CentroUniversitarioRepository,
    ):
        self.repository = repository

    def create_centro(self, data: CentroUniversitarioCreate) -> CentroUniversitario:
        centro = CentroUniversitario.model_validate(data)
        _, total = self.repository.list({"siiau_id": centro.siiau_id})

        if total != 0:
            raise ConflictException(
                "Centro Universitario with that siiau_id already exists."
            )

        return self.repository.create(centro)

    def get_centro(self, centro_id: int) -> CentroUniversitario:
        centro = self.repository.get(centro_id)
        if not centro:
            raise NotFoundException("Centro Universitario not found.")

        return centro

    def list_centros(self, **filters) -> tuple[list[CentroUniversitario], int]:
        return self.repository.list(filters)

    def update_centro(
        self, centro_id: int, data: CentroUniversitarioUpdate
    ) -> CentroUniversitario:
        centro = self.repository.get(centro_id)
        if not centro:
            raise NotFoundException("Centro Universitario not found.")

        update_data = data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            if value is not None:
                setattr(centro, key, value)

        return self.repository.update(centro)

    def delete_centro(self, centro_id) -> None:
        centro = self.repository.get(centro_id)
        if not centro:
            raise NotFoundException("Centro Universitario not found.")

        return self.repository.delete(centro)
