from sqlmodel import Session, select, func, or_
from app.modules.edificio.models import Edificio

class EdificioRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, data: Edificio) -> Edificio:
        self.session.add(data)
        self.session.commit()
        self.session.refresh(data)
        return data

    def get(self, edificio_id: int) -> Edificio | None:
        statement = select(Edificio).where(Edificio.id == edificio_id)
        return self.session.exec(statement).first()

    def list(self, filters: dict) -> tuple[list[Edificio], int]:
        statement = select(Edificio)
        total_statement = select(func.count()).select_from(Edificio)

        if filters.get("centro_id") is not None:
            statement = statement.where(Edificio.centro_id == filters["centro_id"])
            total_statement = total_statement.where(Edificio.centro_id == filters["centro_id"])

        if filters.get("name") is not None:
            statement = statement.where(Edificio.name == filters["name"])
            total_statement = total_statement.where(Edificio.name == filters["name"])

        if filters.get("search"):
            search = f"%{filters['search']}%"
            statement = statement.where(
                or_(
                    Edificio.name.ilike(search),
                )
            )
            total_statement = total_statement.where(
                or_(
                    Edificio.name.ilike(search),
                )
            )

        statement = statement.offset(filters.get("skip", 0)).limit(filters.get("limit", 100))
        edificios = self.session.exec(statement).all()
        total = self.session.exec(total_statement).one()

        return edificios, total

    def update(self, data: Edificio) -> Edificio:
        self.session.add(data)
        self.session.commit()
        self.session.refresh(data)
        return data

    def delete(self, edificio: Edificio) -> None:
        self.session.delete(edificio)
        self.session.commit()
