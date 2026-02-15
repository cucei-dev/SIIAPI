# Development Guide

This guide covers setting up a development environment and contributing to SIIAPI.

## Table of Contents

- [Development Setup](#development-setup)
- [Project Structure](#project-structure)
- [Coding Standards](#coding-standards)
- [Adding New Features](#adding-new-features)
- [Testing](#testing)
- [Database Migrations](#database-migrations)
- [Debugging](#debugging)
- [Git Workflow](#git-workflow)
- [Common Tasks](#common-tasks)

## Development Setup

### Prerequisites

- Python 3.10 or higher
- Git
- Code editor (VS Code recommended)
- Database client (optional but helpful)

### Initial Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd SIIAPI
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   
   # Linux/Mac
   source venv/bin/activate
   
   # Windows
   venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Create `.env` file**:
   ```bash
   cp .env.example .env  # If example exists
   # Or create manually
   ```

   Development `.env`:
   ```env
   DB_URL=sqlite:///./db.sqlite3
   APP_NAME=SIIAPI
   APP_SITE=localhost
   APP_ENV=dev
   APP_DESCRIPTION=University Academic Information API
   APP_DEBUG=true
   SECRET_KEY=dev-secret-key-change-in-production
   DUMMY_HASH=$2b$12$dummy_hash_for_development
   SIIAU_URL=https://siiau.udg.mx/wco/sspseca.consulta_oferta
   ```

5. **Run development server**:
   ```bash
   # Using the dev script
   chmod +x dev.sh
   ./dev.sh
   
   # Or manually
   fastapi dev app/main.py
   ```

6. **Access the application**:
   - API: http://localhost:8000
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### VS Code Setup

#### Recommended Extensions

- Python (Microsoft)
- Pylance
- Python Docstring Generator
- GitLens
- REST Client
- SQLite Viewer (for SQLite databases)

#### Settings (`.vscode/settings.json`)

```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/venv/bin/python",
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": false,
  "python.linting.flake8Enabled": true,
  "python.formatting.provider": "black",
  "editor.formatOnSave": true,
  "editor.rulers": [88],
  "[python]": {
    "editor.tabSize": 4
  }
}
```

#### Launch Configuration (`.vscode/launch.json`)

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "FastAPI",
      "type": "python",
      "request": "launch",
      "module": "uvicorn",
      "args": [
        "app.main:app",
        "--reload",
        "--host",
        "0.0.0.0",
        "--port",
        "8000"
      ],
      "jinja": true,
      "justMyCode": true,
      "env": {
        "PYTHONPATH": "${workspaceFolder}"
      }
    }
  ]
}
```

## Project Structure

```
SIIAPI/
├── app/
│   ├── __init__.py
│   ├── main.py                    # Application entry point
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes.py              # Main router
│   │   ├── dependencies/          # Shared dependencies
│   │   │   ├── auth.py           # Authentication
│   │   │   └── database.py       # Database session
│   │   └── schemas/
│   │       └── pagination.py     # Pagination schemas
│   ├── core/
│   │   ├── config.py             # Configuration
│   │   ├── database.py           # Database setup
│   │   ├── security.py           # Security utilities
│   │   ├── exceptions.py         # Custom exceptions
│   │   └── seed.py               # Data seeding
│   └── modules/
│       └── [module_name]/        # Feature modules
│           ├── api/
│           │   ├── dependencies.py
│           │   └── routes.py
│           ├── models/
│           │   └── [model].py
│           ├── repositories/
│           │   └── [repository].py
│           ├── schemas/
│           │   └── [schema].py
│           └── services/
│               └── [service].py
├── docs/                          # Documentation
├── tests/                         # Test files (to be added)
├── .env                          # Environment variables (not in git)
├── .gitignore
├── requirements.txt
├── dev.sh                        # Development script
└── README.md
```

## Coding Standards

### Python Style Guide

Follow PEP 8 with these specifics:

- **Line Length**: 88 characters (Black default)
- **Indentation**: 4 spaces
- **Quotes**: Double quotes for strings
- **Imports**: Organized (standard library, third-party, local)

### Naming Conventions

```python
# Classes: PascalCase
class UserService:
    pass

# Functions/Methods: snake_case
def get_user_by_id(user_id: int):
    pass

# Variables: snake_case
user_email = "user@example.com"

# Constants: UPPER_SNAKE_CASE
MAX_PAGE_SIZE = 100

# Private: _leading_underscore
def _internal_helper():
    pass
```

### Type Hints

Always use type hints:

```python
from typing import Optional, List

def get_users(
    db: Session,
    skip: int = 0,
    limit: int = 10
) -> List[User]:
    return db.query(User).offset(skip).limit(limit).all()

def get_user(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()
```

### Docstrings

Use Google-style docstrings:

```python
def create_user(db: Session, user: UserCreate) -> User:
    """
    Create a new user in the database.

    Args:
        db: Database session
        user: User creation schema

    Returns:
        Created user object

    Raises:
        ConflictException: If email already exists
    """
    # Implementation
    pass
```

## Adding New Features

### Creating a New Module

1. **Create module structure**:
   ```bash
   mkdir -p app/modules/new_module/{api,models,repositories,schemas,services}
   touch app/modules/new_module/__init__.py
   touch app/modules/new_module/api/{__init__.py,dependencies.py,routes.py}
   touch app/modules/new_module/models/{__init__.py,new_model.py}
   touch app/modules/new_module/repositories/{__init__.py,new_repository.py}
   touch app/modules/new_module/schemas/{__init__.py,new_schema.py}
   touch app/modules/new_module/services/{__init__.py,new_service.py}
   ```

2. **Define the model** (`models/new_model.py`):
   ```python
   from sqlmodel import SQLModel, Field, Relationship
   from pydantic import ConfigDict
   from datetime import datetime

   class NewModel(SQLModel, table=True):
       id: int | None = Field(default=None, primary_key=True)
       name: str = Field(index=True)
       description: str | None = None
       created_at: datetime = Field(default_factory=datetime.now)
       
       # Relationships
       related_items: list["RelatedModel"] = Relationship(back_populates="new_model")
       
       model_config = ConfigDict(from_attributes=True)
   ```

3. **Create schemas** (`schemas/new_schema.py`):
   ```python
   from pydantic import BaseModel
   from datetime import datetime

   class NewModelBase(BaseModel):
       name: str
       description: str | None = None

   class NewModelCreate(NewModelBase):
       pass

   class NewModelUpdate(BaseModel):
       name: str | None = None
       description: str | None = None

   class NewModelRead(NewModelBase):
       id: int
       created_at: datetime
       
       class Config:
           from_attributes = True
   ```

4. **Implement repository** (`repositories/new_repository.py`):
   ```python
   from sqlmodel import Session, select
   from app.modules.new_module.models import NewModel
   from typing import Optional

   class NewModelRepository:
       def __init__(self, db: Session):
           self.db = db

       def create(self, model: NewModel) -> NewModel:
           self.db.add(model)
           self.db.commit()
           self.db.refresh(model)
           return model

       def get(self, model_id: int) -> Optional[NewModel]:
           return self.db.get(NewModel, model_id)

       def list(self, filters: dict = None, skip: int = 0, limit: int = 10):
           query = select(NewModel)
           
           if filters:
               if "name" in filters:
                   query = query.where(NewModel.name.contains(filters["name"]))
           
           total = len(self.db.exec(query).all())
           items = self.db.exec(query.offset(skip).limit(limit)).all()
           
           return items, total

       def update(self, model: NewModel) -> NewModel:
           self.db.add(model)
           self.db.commit()
           self.db.refresh(model)
           return model

       def delete(self, model_id: int) -> bool:
           model = self.get(model_id)
           if model:
               self.db.delete(model)
               self.db.commit()
               return True
           return False
   ```

5. **Create service** (`services/new_service.py`):
   ```python
   from app.modules.new_module.repositories import NewModelRepository
   from app.modules.new_module.schemas import NewModelCreate, NewModelUpdate
   from app.modules.new_module.models import NewModel
   from app.core.exceptions import NotFoundException

   class NewModelService:
       def __init__(self, repository: NewModelRepository):
           self.repository = repository

       def create_model(self, data: NewModelCreate) -> NewModel:
           model = NewModel(**data.model_dump())
           return self.repository.create(model)

       def get_model(self, model_id: int) -> NewModel:
           model = self.repository.get(model_id)
           if not model:
               raise NotFoundException("Model not found")
           return model

       def list_models(self, filters: dict = None, page: int = 1, page_size: int = 10):
           skip = (page - 1) * page_size
           return self.repository.list(filters, skip, page_size)

       def update_model(self, model_id: int, data: NewModelUpdate) -> NewModel:
           model = self.get_model(model_id)
           
           for key, value in data.model_dump(exclude_unset=True).items():
               setattr(model, key, value)
           
           return self.repository.update(model)

       def delete_model(self, model_id: int) -> None:
           if not self.repository.delete(model_id):
               raise NotFoundException("Model not found")
   ```

6. **Create API routes** (`api/routes.py`):
   ```python
   from fastapi import APIRouter, Depends, status
   from app.modules.new_module.schemas import NewModelCreate, NewModelUpdate, NewModelRead
   from app.modules.new_module.services import NewModelService
   from app.modules.new_module.api.dependencies import get_new_model_service
   from app.api.schemas.pagination import PaginationParams

   router = APIRouter()

   @router.post("/", response_model=NewModelRead, status_code=status.HTTP_201_CREATED)
   def create_model(
       data: NewModelCreate,
       service: NewModelService = Depends(get_new_model_service)
   ):
       return service.create_model(data)

   @router.get("/{model_id}", response_model=NewModelRead)
   def get_model(
       model_id: int,
       service: NewModelService = Depends(get_new_model_service)
   ):
       return service.get_model(model_id)

   @router.get("/", response_model=dict)
   def list_models(
       pagination: PaginationParams = Depends(),
       service: NewModelService = Depends(get_new_model_service)
   ):
       items, total = service.list_models(
           page=pagination.page,
           page_size=pagination.page_size
       )
       return {
           "items": items,
           "total": total,
           "page": pagination.page,
           "page_size": pagination.page_size
       }

   @router.put("/{model_id}", response_model=NewModelRead)
   def update_model(
       model_id: int,
       data: NewModelUpdate,
       service: NewModelService = Depends(get_new_model_service)
   ):
       return service.update_model(model_id, data)

   @router.delete("/{model_id}", status_code=status.HTTP_204_NO_CONTENT)
   def delete_model(
       model_id: int,
       service: NewModelService = Depends(get_new_model_service)
   ):
       service.delete_model(model_id)
   ```

7. **Create dependencies** (`api/dependencies.py`):
   ```python
   from fastapi import Depends
   from sqlmodel import Session
   from app.api.dependencies.database import get_db
   from app.modules.new_module.repositories import NewModelRepository
   from app.modules.new_module.services import NewModelService

   def get_new_model_service(db: Session = Depends(get_db)) -> NewModelService:
       repository = NewModelRepository(db)
       return NewModelService(repository)
   ```

8. **Register routes** in `app/api/routes.py`:
   ```python
   from app.modules.new_module.api.routes import router as new_module_router
   
   router.include_router(new_module_router, prefix="/new-module", tags=["New Module"])
   ```

9. **Register model** in `app/core/database.py`:
   ```python
   import app.modules.new_module.models
   ```

## Testing

### Unit Tests

Create `tests/test_new_module.py`:

```python
import pytest
from sqlmodel import Session, create_engine, SQLModel
from app.modules.new_module.models import NewModel
from app.modules.new_module.repositories import NewModelRepository
from app.modules.new_module.services import NewModelService
from app.modules.new_module.schemas import NewModelCreate

@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

def test_create_model(db_session):
    repository = NewModelRepository(db_session)
    service = NewModelService(repository)
    
    data = NewModelCreate(name="Test", description="Test description")
    model = service.create_model(data)
    
    assert model.id is not None
    assert model.name == "Test"
```

### Running Tests

```bash
# Install pytest
pip install pytest pytest-cov

# Run tests
pytest

# With coverage
pytest --cov=app tests/
```

## Database Migrations

Currently using SQLModel's `create_all()`. For production, consider Alembic:

```bash
# Install Alembic
pip install alembic

# Initialize
alembic init alembic

# Create migration
alembic revision --autogenerate -m "Add new table"

# Apply migration
alembic upgrade head
```

## Debugging

### Using Python Debugger

```python
# Add breakpoint
import pdb; pdb.set_trace()

# Or use built-in
breakpoint()
```

### FastAPI Debug Mode

Already enabled in development with `APP_DEBUG=true`.

### Database Query Logging

Enable in `.env`:
```env
APP_DEBUG=true  # Enables SQLAlchemy echo
```

## Git Workflow

### Branch Naming

- `feature/feature-name` - New features
- `bugfix/bug-description` - Bug fixes
- `hotfix/critical-fix` - Critical production fixes
- `refactor/what-changed` - Code refactoring

### Commit Messages

Follow conventional commits:

```
type(scope): subject

body (optional)

footer (optional)
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

Examples:
```
feat(auth): add password reset functionality
fix(users): resolve email validation issue
docs(api): update authentication endpoints
```

### Pull Request Process

1. Create feature branch
2. Make changes
3. Write tests
4. Update documentation
5. Create pull request
6. Code review
7. Merge to main

## Common Tasks

### Reset Database

```bash
rm db.sqlite3
python -c "from app.core.database import init_db; from app.core.seed import seed_data; init_db(); seed_data()"
```

### Generate Dummy Hash

```python
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
print(pwd_context.hash("dummy"))
```

### Test API Endpoint

```bash
# Using curl
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password"}'

# Using httpie
http POST localhost:8000/api/auth/login email=user@example.com password=password
```

### Check Code Style

```bash
# Install tools
pip install black flake8 isort

# Format code
black app/

# Check style
flake8 app/

# Sort imports
isort app/
```

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)

---

For questions or issues, please open an issue on the repository.