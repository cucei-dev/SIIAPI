from sqlmodel import Session, select, func, or_
from app.modules.profesor.models import Profesor

class ProfesorRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, data: Profesor) -> Profesor:
        self.session.add(data)
        self.session.commit()
        self.session.refresh(data)
        return data

    def get(self, profesor_id: int) -> Profesor | None:
        statement = select(Profesor).where(Profesor.id == profesor_id)
        return self.session.exec(statement).first()

    def list(self, filters: dict) -> tuple[list[Profesor], int]:
        statement = select(Profesor)
        total_statement = select(func.count()).select_from(Profesor)

        if filters.get("name") is not None:
            statement = statement.where(Profesor.name == filters["name"])
            total_statement = total_statement.where(Profesor.name == filters["name"])

        if filters.get("search"):
            search = f"%{filters['search']}%"
            statement = statement.where(
                or_(
                    Profesor.name.ilike(search),
                )
            )
            total_statement = total_statement.where(
                or_(
                    Profesor.name.ilike(search),
                )
            )

        statement = statement.offset(filters.get("skip", 0)).limit(filters.get("limit", 100))
        profesores = self.session.exec(statement).all()
        total = self.session.exec(total_statement).one()

        return profesores, total

    def update(self, data: Profesor) -> Profesor:
        self.session.add(data)
        self.session.commit()
        self.session.refresh(data)
        return data

    def delete(self, profesor: Profesor) -> None:
        self.session.delete(profesor)
        self.session.commit()
