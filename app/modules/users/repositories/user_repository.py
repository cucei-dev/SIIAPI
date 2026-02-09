from sqlmodel import Session, select, func, or_
from app.modules.users.models import User
from datetime import datetime

class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, data: User) -> User:
        self.session.add(data)
        self.session.commit()
        self.session.refresh(data)
        return data

    def get(self, user_id: int) -> User | None:
        statement = select(User).where(User.id == user_id)
        return self.session.exec(statement).first()

    def list(self, filters: dict) -> tuple[list[User], int]:
        statement = select(User)
        total_statement = select(func.count()).select_from(User)

        if filters.get("email"):
            statement = statement.where(User.email == filters["email"])
            total_statement = total_statement.where(User.email == filters["email"])

        if filters.get("is_active") is not None:
            statement = statement.where(User.is_active == filters["is_active"])
            total_statement = total_statement.where(User.is_active == filters["is_active"])

        if filters.get("is_superuser") is not None:
            statement = statement.where(User.is_superuser == filters["is_superuser"])
            total_statement = total_statement.where(User.is_superuser == filters["is_superuser"])

        if filters.get("is_staff") is not None:
            statement = statement.where(User.is_staff == filters["is_staff"])
            total_statement = total_statement.where(User.is_staff == filters["is_staff"])

        if filters.get("search"):
            search = f"%{filters['search']}%"
            statement = statement.where(
                or_(
                    User.email.ilike(search),
                    User.name.ilike(search),
                )
            )
            total_statement = total_statement.where(
                or_(
                    User.email.ilike(search),
                    User.name.ilike(search),
                )
            )

        statement = statement.offset(filters.get("skip", 0)).limit(filters.get("limit", 100))
        users = self.session.exec(statement).all()
        total = self.session.exec(total_statement).one()

        return users, total

    def update(self, data: User) -> User:
        data.updated_at = datetime.now()
        data.credits = round(data.credits, 4)

        self.session.add(data)
        self.session.commit()
        self.session.refresh(data)
        return data

    def delete(self, user: User) -> None:
        self.session.delete(user)
        self.session.commit()
