from sqlmodel import Session, func, or_, select

from app.modules.centro.models import CentroUniversitario


class CentroUniversitarioRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, data: CentroUniversitario) -> CentroUniversitario:
        self.session.add(data)
        self.session.commit()
        self.session.refresh(data)
        return data

    def get(self, centro_id: int) -> CentroUniversitario | None:
        statement = select(CentroUniversitario).where(
            CentroUniversitario.id == centro_id
        )
        return self.session.exec(statement).first()

    def list(self, filters: dict) -> tuple[list[CentroUniversitario], int]:
        statement = select(CentroUniversitario)
        total_statement = select(func.count()).select_from(CentroUniversitario)

        if filters.get("siiau_id") is not None:
            statement = statement.where(
                CentroUniversitario.siiau_id == filters["siiau_id"]
            )
            total_statement = total_statement.where(
                CentroUniversitario.siiau_id == filters["siiau_id"]
            )

        if filters.get("search"):
            search = f"%{filters['search']}%"
            statement = statement.where(
                or_(
                    CentroUniversitario.name.ilike(search),
                )
            )
            total_statement = total_statement.where(
                or_(
                    CentroUniversitario.name.ilike(search),
                )
            )

        statement = statement.offset(filters.get("skip", 0)).limit(
            filters.get("limit", 100)
        )
        centros = self.session.exec(statement).all()
        total = self.session.exec(total_statement).one()

        return centros, total

    def update(self, data: CentroUniversitario) -> CentroUniversitario:
        self.session.add(data)
        self.session.commit()
        self.session.refresh(data)
        return data

    def delete(self, centro: CentroUniversitario) -> None:
        self.session.delete(centro)
        self.session.commit()
