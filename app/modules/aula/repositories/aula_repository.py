from sqlmodel import Session, select, func, or_
from app.modules.aula.models import Aula

class AulaRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, data: Aula) -> Aula:
        self.session.add(data)
        self.session.commit()
        self.session.refresh(data)
        return data

    def get(self, aula_id: int) -> Aula | None:
        statement = select(Aula).where(Aula.id == aula_id)
        return self.session.exec(statement).first()

    def list(self, filters: dict) -> tuple[list[Aula], int]:
        statement = select(Aula)
        total_statement = select(func.count()).select_from(Aula)

        if filters.get("edificio_id") is not None:
            statement = statement.where(Aula.edificio_id == filters["edificio_id"])
            total_statement = total_statement.where(Aula.edificio_id == filters["edificio_id"])

        if filters.get("search"):
            search = f"%{filters['search']}%"
            statement = statement.where(
                or_(
                    Aula.name.ilike(search),
                )
            )
            total_statement = total_statement.where(
                or_(
                    Aula.name.ilike(search),
                )
            )

        statement = statement.offset(filters.get("skip", 0)).limit(filters.get("limit", 100))
        aulas = self.session.exec(statement).all()
        total = self.session.exec(total_statement).one()

        return aulas, total

    def update(self, data: Aula) -> Aula:
        self.session.add(data)
        self.session.commit()
        self.session.refresh(data)
        return data

    def delete(self, aula: Aula) -> None:
        self.session.delete(aula)
        self.session.commit()
