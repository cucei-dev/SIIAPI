from sqlmodel import Session, select, func, or_
from app.modules.materia.models import Materia

class MateriaRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, data: Materia) -> Materia:
        self.session.add(data)
        self.session.commit()
        self.session.refresh(data)
        return data

    def get(self, materia_id: int) -> Materia | None:
        statement = select(Materia).where(Materia.id == materia_id)
        return self.session.exec(statement).first()

    def list(self, filters: dict) -> tuple[list[Materia], int]:
        statement = select(Materia)
        total_statement = select(func.count()).select_from(Materia)

        if filters.get("clave") is not None:
            statement = statement.where(Materia.clave == filters["clave"])
            total_statement = total_statement.where(Materia.clave == filters["clave"])

        if filters.get("search"):
            search = f"%{filters['search']}%"
            statement = statement.where(
                or_(
                    Materia.name.ilike(search),
                )
            )
            total_statement = total_statement.where(
                or_(
                    Materia.name.ilike(search),
                )
            )

        statement = statement.offset(filters.get("skip", 0)).limit(filters.get("limit", 100))
        materias = self.session.exec(statement).all()
        total = self.session.exec(total_statement).one()

        return materias, total

    def update(self, data: Materia) -> Materia:
        self.session.add(data)
        self.session.commit()
        self.session.refresh(data)
        return data

    def delete(self, materia: Materia) -> None:
        self.session.delete(materia)
        self.session.commit()
