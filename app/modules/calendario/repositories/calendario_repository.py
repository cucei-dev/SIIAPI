from sqlmodel import Session, select, func, or_
from app.modules.calendario.models import Calendario

class CalendarioRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, data: Calendario) -> Calendario:
        self.session.add(data)
        self.session.commit()
        self.session.refresh(data)
        return data

    def get(self, calendario_id: int) -> Calendario | None:
        statement = select(Calendario).where(Calendario.id == calendario_id)
        return self.session.exec(statement).first()

    def list(self, filters: dict) -> tuple[list[Calendario], int]:
        statement = select(Calendario)
        total_statement = select(func.count()).select_from(Calendario)

        if filters.get("siiau_id") is not None:
            statement = statement.where(Calendario.siiau_id == filters["siiau_id"])
            total_statement = total_statement.where(Calendario.siiau_id == filters["siiau_id"])

        if filters.get("search"):
            search = f"%{filters['search']}%"
            statement = statement.where(
                or_(
                    Calendario.name.ilike(search),
                )
            )
            total_statement = total_statement.where(
                or_(
                    Calendario.name.ilike(search),
                )
            )

        statement = statement.offset(filters.get("skip", 0)).limit(filters.get("limit", 100))
        calendarios = self.session.exec(statement).all()
        total = self.session.exec(total_statement).one()

        return calendarios, total

    def update(self, data: Calendario) -> Calendario:
        self.session.add(data)
        self.session.commit()
        self.session.refresh(data)
        return data

    def delete(self, calendario: Calendario) -> None:
        self.session.delete(calendario)
        self.session.commit()
