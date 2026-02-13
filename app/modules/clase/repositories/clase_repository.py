from sqlmodel import Session, select, func
from app.modules.clase.models import Clase

class ClaseRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, data: Clase) -> Clase:
        self.session.add(data)
        self.session.commit()
        self.session.refresh(data)
        return data

    def get(self, clase_id: int) -> Clase | None:
        statement = select(Clase).where(Clase.id == clase_id)
        return self.session.exec(statement).first()

    def list(self, filters: dict) -> tuple[list[Clase], int]:
        statement = select(Clase)
        total_statement = select(func.count()).select_from(Clase)

        if filters.get("seccion_id") is not None:
            statement = statement.where(Clase.seccion_id == filters["seccion_id"])
            total_statement = total_statement.where(Clase.seccion_id == filters["seccion_id"])

        if filters.get("aula_id") is not None:
            statement = statement.where(Clase.aula_id == filters["aula_id"])
            total_statement = total_statement.where(Clase.aula_id == filters["aula_id"])

        statement = statement.offset(filters.get("skip", 0)).limit(filters.get("limit", 100))
        clases = self.session.exec(statement).all()
        total = self.session.exec(total_statement).one()

        return clases, total

    def update(self, data: Clase) -> Clase:
        self.session.add(data)
        self.session.commit()
        self.session.refresh(data)
        return data

    def delete(self, clase: Clase) -> None:
        self.session.delete(clase)
        self.session.commit()
