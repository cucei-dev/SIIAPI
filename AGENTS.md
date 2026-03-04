# AGENTS.md - Development Guidelines for SIIAPI

## Overview

SIIAPI is a FastAPI-based REST API for managing university academic information. This file contains guidelines for agentic coding agents working on this codebase.

## Project Structure

```
SIIAPI/
├── app/
│   ├── api/           # API routes and dependencies
│   ├── core/         # Core utilities (config, database, security, exceptions)
│   └── modules/      # Feature modules (auth, users, clase, edificio, etc.)
├── tests/
│   ├── unit/         # Unit tests
│   └── integration/  # Integration tests
├── alembic/          # Database migrations
└── scripts/          # Utility scripts
```

Each module follows: `api/routes.py`, `models/`, `repositories/`, `schemas/`, `services/`

---

## Commands

### Installation
```bash
make install          # Install all dependencies
```

### Running the Application
```bash
make dev             # Start dev server with uvicorn (recommended)
fastapi dev app/main.py  # Alternative: use fastapi CLI
```

### Testing
```bash
make test            # Run all tests
make test-unit       # Run unit tests only
make test-integration  # Run integration tests only
make test-cov       # Run tests with coverage report
```

**Running a single test:**
```bash
# Run specific test file
pytest tests/unit/users/test_user_service.py

# Run specific test class
pytest tests/unit/users/test_user_service.py::TestUserServiceCreate

# Run specific test function
pytest tests/unit/users/test_user_service.py::TestUserServiceCreate::test_create_user_success

# Run by marker
pytest -m unit
pytest -m integration
```

### Linting & Formatting
```bash
make lint            # Run flake8, black --check, isort --check-only
make format          # Run black and isort
```

### Database
```bash
make db-init         # Initialize database (dev mode)
make db-seed         # Seed database with test data
make migrate         # Run Alembic migrations
make migrate-create  # Create new migration (autogenerate)
```

---

## Code Style Guidelines

### General Principles
- Use **Python 3.10+** features (type hints, match/case)
- Follow **SOLID** principles and separation of concerns
- Keep functions small and focused (< 50 lines when possible)
- Use **async/await** for I/O-bound operations

### Imports

**Order (use `isort` to enforce):**
1. Standard library
2. Third-party packages
3. Local application imports

```python
# Standard library
from datetime import datetime
from typing import Generator

# Third-party
from fastapi import APIRouter, Depends
from sqlmodel import Session, select

# Local application
from app.core.exceptions import NotFoundException
from app.modules.users.models import User
from app.modules.users.schemas import UserCreate
```

### Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Modules | snake_case | `user_service.py` |
| Classes | PascalCase | `UserService` |
| Functions | snake_case | `get_user()` |
| Variables | snake_case | `user_id` |
| Constants | UPPER_SNAKE | `MAX_RETRY_COUNT` |
| Database tables | PascalCase | `User` (SQLModel) |

### Type Hints

Always use type hints for function signatures:

```python
# Good
def get_user(user_id: int) -> User | None:
    ...

def list_users(email: str | None = None, skip: int = 0, limit: int = 100) -> tuple[list[User], int]:
    ...

# Bad (no types)
def get_user(user_id):
    ...
```

Use `|` instead of `Union` for Python 3.10+:
```python
# Good
user_id: int | None

# Avoid
user_id: Optional[int]
```

### Error Handling

Use custom exceptions from `app/core/exceptions.py`:

```python
from app.core.exceptions import (
    BadRequestException,
    NotFoundException,
    ConflictException,
    UnauthorizedException,
    ForbiddenException,
)

# In services
def get_user(self, user_id: int) -> User:
    user = self.repository.get(user_id)
    if not user:
        raise NotFoundException("User not found.")
    return user
```

### Pydantic Schemas

- Use `BaseModel` or SQLModel for request/response validation
- Use `Field()` for validation and constraints
- Use `ConfigDict(from_attributes=True)` for ORM compatibility

```python
from pydantic import ConfigDict, Field
from sqlmodel import SQLModel

class UserCreate(SQLModel):
    name: str = Field(min_length=1, max_length=100)
    email: str = Field(pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")
    password: str = Field(min_length=8)

    model_config = ConfigDict(from_attributes=True)
```

### Database Access (Repository Pattern)

Always use the repository pattern for data access:

```python
# Repository layer
class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def get(self, user_id: int) -> User | None:
        statement = select(User).where(User.id == user_id)
        return self.session.exec(statement).first()

# Service layer (uses repository)
class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def get_user(self, user_id: int) -> User:
        user = self.repository.get(user_id)
        if not user:
            raise NotFoundException("User not found.")
        return user
```

### API Routes

```python
from fastapi import APIRouter, Depends, Query, status

router = APIRouter()

@router.get("/", response_model=Pagination[UserRead])
async def list_users(
    skip: int = 0,
    limit: int = Query(default=100, ge=1, le=100),
    service: UserService = Depends(get_user_service),
):
    users, total = service.list_users(skip=skip, limit=limit)
    return Pagination(total=total, results=users)
```

### Testing Guidelines

- Mark tests with pytest markers: `@pytest.mark.unit` or `@pytest.mark.integration`
- Use fixtures from `tests/conftest.py`
- Use descriptive test names: `test_create_user_success`, `test_create_user_duplicate_email`

```python
@pytest.mark.unit
class TestUserServiceCreate:
    def test_create_user_success(self, session: Session):
        """Test successful user creation"""
        ...
```

### Configuration

All configuration goes in `app/core/config.py`. Use environment variables:

```python
class Settings:
    DB_URL: str = os.getenv("DB_URL", "sqlite:///./db.sqlite3")
    APP_DEBUG: bool = get_bool(os.getenv("APP_DEBUG", "true"))
    SECRET_KEY: str = os.getenv("SECRET_KEY")

settings = Settings()
```

---

## Key Files

- `app/main.py` - FastAPI application entry point
- `app/core/config.py` - Application settings
- `app/core/database.py` - Database initialization
- `app/core/exceptions.py` - Custom HTTP exceptions
- `app/core/security.py` - JWT and password utilities
- `app/api/routes.py` - Main API router
- `pytest.ini` - Pytest configuration

---

## Notes

- The project uses **SQLModel** (combines SQLAlchemy + Pydantic)
- Authentication uses JWT with refresh tokens
- Development mode (`APP_DEBUG=true`) auto-creates tables and seeds data
- Production uses Alembic migrations
