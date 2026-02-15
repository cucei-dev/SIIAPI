from app.core.exceptions import ConflictException, NotFoundException
from app.modules.calendario.repositories.calendario_repository import \
    CalendarioRepository
from app.modules.centro.repositories.centro_repository import \
    CentroUniversitarioRepository
from app.modules.materia.repositories.materia_repository import \
    MateriaRepository
from app.modules.profesor.repositories.profesor_repository import \
    ProfesorRepository
from app.modules.seccion.models import Seccion
from app.modules.seccion.repositories.seccion_repository import \
    SeccionRepository
from app.modules.seccion.schemas import SeccionCreate, SeccionUpdate


class SeccionService:
    def __init__(
        self,
        repository: SeccionRepository,
        calendario_repository: CalendarioRepository,
        centro_repository: CentroUniversitarioRepository,
        materia_repository: MateriaRepository,
        profesor_repository: ProfesorRepository,
    ):
        self.repository = repository
        self.calendario_repository = calendario_repository
        self.centro_repository = centro_repository
        self.materia_repository = materia_repository
        self.profesor_repository = profesor_repository

    def create_seccion(self, data: SeccionCreate) -> Seccion:
        seccion = Seccion.model_validate(data)
        calendario = self.calendario_repository.get(seccion.calendario_id)

        if not calendario:
            raise NotFoundException("Calendario not found.")

        centro = self.centro_repository.get(seccion.centro_id)

        if not centro:
            raise NotFoundException("Centro Universitario not found.")

        materia = self.materia_repository.get(seccion.materia_id)

        if not materia:
            raise NotFoundException("Materia not found.")

        if seccion.profesor_id is not None:
            profesor = self.profesor_repository.get(seccion.profesor_id)

            if not profesor:
                raise NotFoundException("Profesor not found.")

        _, total = self.repository.list(
            {"nrc": seccion.nrc, "calendario_id": seccion.calendario_id}
        )

        if total != 0:
            raise ConflictException(
                "Seccion with that nrc in that Calendario already exists."
            )
        return self.repository.create(seccion)

    def get_seccion(self, seccion_id: int) -> Seccion:
        seccion = self.repository.get(seccion_id)
        if not seccion:
            raise NotFoundException("Sección not found.")

        return seccion

    def list_secciones(self, **filters) -> tuple[list[Seccion], int]:
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
