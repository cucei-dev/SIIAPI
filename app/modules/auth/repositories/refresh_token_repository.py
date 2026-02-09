from sqlmodel import Session, select, func
from app.modules.auth.models import RefreshToken
from datetime import datetime

class RefreshTokenRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, data: RefreshToken) -> RefreshToken:
        self.session.add(data)
        self.session.commit()
        self.session.refresh(data)
        return data

    def get(self, refresh_token_id: int) -> RefreshToken | None:
        statement = select(RefreshToken).where(RefreshToken.id == refresh_token_id)
        return self.session.exec(statement).first()

    def list(self, filters: dict) -> tuple[list[RefreshToken], int]:
        statement = select(RefreshToken)
        total_statement = select(func.count()).select_from(RefreshToken)

        if filters.get("user_id"):
            statement = statement.where(RefreshToken.user_id == filters["user_id"])
            total_statement = total_statement.where(RefreshToken.user_id == filters["user_id"])

        if filters.get("jti"):
            statement = statement.where(RefreshToken.jti == filters["jti"])
            total_statement = total_statement.where(RefreshToken.jti == filters["jti"])

        if filters.get("token_hash"):
            statement = statement.where(RefreshToken.token_hash == filters["token_hash"])
            total_statement = total_statement.where(RefreshToken.token_hash == filters["token_hash"])

        if filters.get("expired") is not None:
            if filters["expired"]:
                statement = statement.where(RefreshToken.expires_at < datetime.now())
                total_statement = total_statement.where(RefreshToken.expires_at < datetime.now())
            else:
                statement = statement.where(RefreshToken.expires_at > datetime.now())
                total_statement = total_statement.where(RefreshToken.expires_at > datetime.now())

        if filters.get("is_active") is not None:
            statement = statement.where(RefreshToken.is_active == filters["is_active"])
            total_statement = total_statement.where(RefreshToken.is_active == filters["is_active"])

        if filters.get("user_agent"):
            statement = statement.where(RefreshToken.user_agent == filters["user_agent"])
            total_statement = total_statement.where(RefreshToken.user_agent == filters["user_agent"])

        if filters.get("ip_address"):
            statement = statement.where(RefreshToken.ip_address == filters["ip_address"])
            total_statement = total_statement.where(RefreshToken.ip_address == filters["ip_address"])

        statement = statement.offset(filters.get("skip", 0)).limit(filters.get("limit", 100))
        refresh_tokens = self.session.exec(statement).all()
        total = self.session.exec(total_statement).one()

        return refresh_tokens, total

    def update(self, data: RefreshToken) -> RefreshToken:
        self.session.add(data)
        self.session.commit()
        self.session.refresh(data)
        return data

    def delete(self, refresh_token: RefreshToken) -> None:
        self.session.delete(refresh_token)
        self.session.commit()
