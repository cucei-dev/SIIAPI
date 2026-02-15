"""
Pytest configuration and fixtures for the test suite
"""

from typing import Generator
from unittest.mock import Mock

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from app.api.dependencies.database import get_session
from app.core.database import engine as production_engine
from app.core.security import create_access_token, hash_password
from app.main import app
from app.modules.auth.models import RefreshToken
from app.modules.auth.schemas import AccessTokenData
from app.modules.users.models import User


# Test database engine with in-memory SQLite
@pytest.fixture(name="test_engine")
def test_engine_fixture():
    """Create a test database engine"""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    return engine


@pytest.fixture(name="session")
def session_fixture(test_engine) -> Generator[Session, None, None]:
    """Create a test database session"""
    with Session(test_engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session) -> Generator[TestClient, None, None]:
    """Create a test client with overridden dependencies"""

    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture(name="test_user")
def test_user_fixture(session: Session) -> User:
    """Create a test user"""
    user = User(
        name="Test User",
        email="test@example.com",
        password=hash_password("testpassword123"),
        is_active=True,
        is_superuser=False,
        is_staff=False,
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@pytest.fixture(name="test_superuser")
def test_superuser_fixture(session: Session) -> User:
    """Create a test superuser"""
    user = User(
        name="Admin User",
        email="admin@example.com",
        password=hash_password("adminpassword123"),
        is_active=True,
        is_superuser=True,
        is_staff=True,
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@pytest.fixture(name="test_inactive_user")
def test_inactive_user_fixture(session: Session) -> User:
    """Create an inactive test user"""
    user = User(
        name="Inactive User",
        email="inactive@example.com",
        password=hash_password("inactivepassword123"),
        is_active=False,
        is_superuser=False,
        is_staff=False,
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@pytest.fixture(name="auth_headers")
def auth_headers_fixture(test_user: User) -> dict:
    """Create authentication headers for test user"""
    access_token = create_access_token(
        AccessTokenData(
            sub=test_user.email,
            is_superuser=test_user.is_superuser,
            is_staff=test_user.is_staff,
            aud="test",
        )
    )
    return {"Authorization": f"Bearer {access_token.token}"}


@pytest.fixture(name="superuser_auth_headers")
def superuser_auth_headers_fixture(test_superuser: User) -> dict:
    """Create authentication headers for superuser"""
    access_token = create_access_token(
        AccessTokenData(
            sub=test_superuser.email,
            is_superuser=test_superuser.is_superuser,
            is_staff=test_superuser.is_staff,
            aud="test",
        )
    )
    return {"Authorization": f"Bearer {access_token.token}"}


@pytest.fixture(name="mock_session")
def mock_session_fixture():
    """Create a mock database session"""
    return Mock(spec=Session)


@pytest.fixture(autouse=True)
def reset_database(session: Session):
    """Reset database before each test"""
    yield
    # Cleanup after test
    session.rollback()
