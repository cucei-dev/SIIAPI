from app.modules.calendario.repositories.calendario_repository import CalendarioRepository
from app.modules.calendario.schemas import CalendarioCreate, CalendarioUpdate
from app.modules.calendario.models import Calendario
from app.core.exceptions import NotFoundException, ConflictException

class CalendarioService:
    def __init__(
        self,
        repository: CalendarioRepository,
    ):
        self.repository = repository

    def create_calendario(self, data: CalendarioCreate) -> Calendario:
        calendario = Calendario.model_validate(data)
        _,total = self.repository.list({"siiau_id": calendario.siiau_id})

        if total != 0:
            raise ConflictException("Calendario with that siiau_id already exists.")

        return self.repository.create(calendario)

    def get_calendario(self, calendario_id: int) -> Calendario:
        calendario = self.repository.get(calendario_id)
        if not calendario:
            raise NotFoundException("Calendario not found.")

        return calendario

    def list_calendarios(self, **filters) -> tuple[list[Calendario], int]:
        return self.repository.list(filters)

    def update_calendario(self, calendario_id: int, data: CalendarioUpdate) -> Calendario:
        calendario = self.repository.get(calendario_id)
        if not calendario:
            raise NotFoundException("Calendario not found.")

        update_data = data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            if value is not None:
                setattr(calendario, key, value)

        return self.repository.update(calendario)

    def delete_calendario(self, calendario_id) -> None:
        calendario = self.repository.get(calendario_id)
        if not calendario:
            raise NotFoundException("Calendario not found.")

        return self.repository.delete(calendario)
