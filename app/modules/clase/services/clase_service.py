from app.modules.clase.repositories.clase_repository import ClaseRepository
from app.modules.clase.schemas import ClaseCreate, ClaseUpdate
from app.modules.clase.models import Clase
from app.core.exceptions import NotFoundException, ConflictException
from app.modules.seccion.repositories.seccion_repository import SeccionRepository
from app.modules.aula.repositories.aula_repository import AulaRepository

class ClaseService:
    def __init__(
        self,
        repository: ClaseRepository,
        seccion_repository: SeccionRepository,
        aula_repository: AulaRepository,
    ):
        self.repository = repository
        self.seccion_repository = seccion_repository
        self.aula_repository = aula_repository

    def create_clase(self, data: ClaseCreate) -> Clase:
        clase = Clase.model_validate(data)
        seccion = self.seccion_repository.get(clase.seccion_id)

        if not seccion:
            raise NotFoundException("Sección not found.")

        _,total = self.repository.list(
            {
                "seccion_id": clase.seccion_id,
                "aula_id": clase.aula_id,
                "hora_inicio": clase.hora_inicio,
                "hora_fin": clase.hora_fin,
                "dia": clase.dia,
            }
        )

        if total != 0 and (
            clase.seccion_id is not None and
            clase.aula_id is not None and
            clase.hora_inicio is not None and
            clase.hora_fin is not None and
            clase.dia is not None
        ):
            raise ConflictException("A clase with same parameters already exists.")
        return self.repository.create(clase)

    def get_clase(self, clase_id: int) -> Clase:
        clase = self.repository.get(clase_id)
        if not clase:
            raise NotFoundException("Clase not found.")

        return clase

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
