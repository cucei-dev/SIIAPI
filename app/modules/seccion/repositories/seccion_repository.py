from sqlmodel import Session, func, or_, select

from app.modules.seccion.models import Seccion


class SeccionRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, data: Seccion) -> Seccion:
        self.session.add(data)
        self.session.commit()
        self.session.refresh(data)
        return data

    def get(self, seccion_id: int) -> Seccion | None:
        statement = select(Seccion).where(Seccion.id == seccion_id)
        return self.session.exec(statement).first()

    def list(self, filters: dict) -> tuple[list[Seccion], int]:
        statement = select(Seccion)
        total_statement = select(func.count()).select_from(Seccion)

        if filters.get("nrc") is not None:
            statement = statement.where(Seccion.nrc == filters["nrc"])
            total_statement = total_statement.where(Seccion.nrc == filters["nrc"])

        if filters.get("centro_id") is not None:
            statement = statement.where(Seccion.centro_id == filters["centro_id"])
            total_statement = total_statement.where(
                Seccion.centro_id == filters["centro_id"]
            )

        if filters.get("materia_id") is not None:
            statement = statement.where(Seccion.materia_id == filters["materia_id"])
            total_statement = total_statement.where(
                Seccion.materia_id == filters["materia_id"]
            )

        if filters.get("profesor_id") is not None:
            statement = statement.where(Seccion.profesor_id == filters["profesor_id"])
            total_statement = total_statement.where(
                Seccion.profesor_id == filters["profesor_id"]
            )

        if filters.get("calendario_id") is not None:
            statement = statement.where(
                Seccion.calendario_id == filters["calendario_id"]
            )
            total_statement = total_statement.where(
                Seccion.calendario_id == filters["calendario_id"]
            )

        if filters.get("search"):
            search = f"%{filters['search']}%"
            statement = statement.where(
                or_(
                    Seccion.name.ilike(search),
                )
            )
            total_statement = total_statement.where(
                or_(
                    Seccion.name.ilike(search),
                )
            )

        statement = statement.offset(filters.get("skip", 0)).limit(
            filters.get("limit", 100)
        )
        secciones = self.session.exec(statement).all()
        total = self.session.exec(total_statement).one()

        return secciones, total

    def update(self, data: Seccion) -> Seccion:
        self.session.add(data)
        self.session.commit()
        self.session.refresh(data)
        return data

    def delete(self, seccion: Seccion) -> None:
        self.session.delete(seccion)
        self.session.commit()
