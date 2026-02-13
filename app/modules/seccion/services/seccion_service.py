from app.modules.seccion.repositories.seccion_repository import SeccionRepository
from app.modules.seccion.schemas import SeccionCreate, SeccionUpdate
from app.modules.seccion.models import Seccion
from app.core.exceptions import NotFoundException, ConflictException

class SeccionService:
    def __init__(
        self,
        repository: SeccionRepository,
    ):
        self.repository = repository

    def create_seccion(self, data: SeccionCreate) -> Seccion:
        seccion = Seccion.model_validate(data)
        return self.repository.create(seccion)

    def get_seccion(self, seccion_id: int):
        seccion = self.repository.get(seccion_id)
        if not seccion:
            raise NotFoundException("Sección not found.")

    def list_seccions(self, **filters) -> tuple[list[Seccion], int]:
        return self.repository.list(filters)

    def update_seccion(self, seccion_id: int, data: SeccionUpdate) -> Seccion:
        seccion = self.repository.get(seccion_id)
        if not seccion:
            raise NotFoundException("Sección not found.")

        update_data = data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            if value is not None:
                setattr(seccion, key, value)

        return self.repository.update(seccion)

    def delete_seccion(self, seccion_id) -> None:
        seccion = self.repository.get(seccion_id)
        if not seccion:
            raise NotFoundException("Sección not found.")

        return self.repository.delete(seccion)
