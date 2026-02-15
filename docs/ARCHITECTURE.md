# SIIAPI Architecture Documentation

## Overview

SIIAPI is built using a modular, layered architecture following Domain-Driven Design (DDD) principles and clean architecture patterns. The application is structured to ensure separation of concerns, maintainability, and scalability.

## Architecture Layers

### 1. Presentation Layer (API)
- **Location**: `app/modules/*/api/`
- **Responsibility**: HTTP request/response handling
- **Components**:
  - Route handlers (FastAPI endpoints)
  - Request validation (Pydantic schemas)
  - Response serialization
  - Dependency injection

### 2. Business Logic Layer (Services)
- **Location**: `app/modules/*/services/`
- **Responsibility**: Business rules and orchestration
- **Components**:
  - Service classes containing business logic
  - Data transformation
  - Cross-module coordination
  - Transaction management

### 3. Data Access Layer (Repositories)
- **Location**: `app/modules/*/repositories/`
- **Responsibility**: Database operations
- **Components**:
  - CRUD operations
  - Query building
  - Data filtering and pagination
  - Database session management

### 4. Domain Layer (Models)
- **Location**: `app/modules/*/models/`
- **Responsibility**: Domain entities and business objects
- **Components**:
  - SQLModel database models
  - Entity relationships
  - Domain constraints

### 5. Schema Layer
- **Location**: `app/modules/*/schemas/`
- **Responsibility**: Data validation and serialization
- **Components**:
  - Request schemas (Create, Update)
  - Response schemas (Read, List)
  - Validation rules

## Core Components

### Application Core (`app/core/`)

#### config.py
- Environment variable management
- Application settings
- Configuration validation
- Type conversion utilities

#### database.py
- Database engine creation
- Connection management
- Model registration
- Table initialization

#### security.py
- Password hashing (bcrypt)
- JWT token generation and validation
- Symmetric encryption/decryption
- Security utilities

#### exceptions.py
- Custom exception classes
- HTTP exception mapping
- Error handling utilities

#### seed.py
- Development data seeding
- Initial data population
- Test data generation

## Module Architecture

Each module follows a consistent structure:

```
module_name/
├── __init__.py
├── api/
│   ├── __init__.py
│   ├── dependencies.py      # Module-specific dependencies
│   └── routes.py            # API endpoints
├── models/
│   ├── __init__.py
│   └── model_name.py        # Database models
├── repositories/
│   ├── __init__.py
│   └── repository.py        # Data access
├── schemas/
│   ├── __init__.py
│   └── schema.py            # Validation schemas
└── services/
    ├── __init__.py
    └── service.py           # Business logic
```

## Data Flow

### Request Flow
```
Client Request
    ↓
API Route (routes.py)
    ↓
Dependency Injection (dependencies.py)
    ↓
Service Layer (service.py)
    ↓
Repository Layer (repository.py)
    ↓
Database (SQLModel)
    ↓
Response (schemas.py)
    ↓
Client Response
```

### Example: Creating a Section

1. **Client** sends POST request to `/api/secciones`
2. **Route Handler** validates request using `SeccionCreate` schema
3. **Dependency** injects database session and service
4. **Service** applies business logic (validation, transformation)
5. **Repository** executes database INSERT
6. **Model** represents the database entity
7. **Schema** serializes response using `SeccionRead`
8. **Client** receives JSON response

## Database Design

### Entity Relationships

```
User ──< RefreshToken

Calendario ──< Seccion
Centro ──< Seccion
Centro ──< Edificio
Materia ──< Seccion
Profesor ──< Seccion

Seccion ──< Clase

Edificio ──< Aula
Aula ──< Clase
```

### Key Relationships

- **One-to-Many**: User → RefreshTokens
- **One-to-Many**: Calendario → Secciones
- **One-to-Many**: Centro → Secciones, Edificios
- **One-to-Many**: Materia → Secciones
- **One-to-Many**: Profesor → Secciones
- **One-to-Many**: Seccion → Clases
- **One-to-Many**: Edificio → Aulas
- **One-to-Many**: Aula → Clases

### Cascade Deletes

All relationships use `CASCADE DELETE` to maintain referential integrity:
- Deleting a User removes all their RefreshTokens
- Deleting a Centro removes all associated Secciones and Edificios
- Deleting a Seccion removes all associated Clases
- And so on...

## Authentication & Authorization

### JWT Token System

#### Access Token
```json
{
  "sub": "user@example.com",
  "is_superuser": false,
  "is_staff": false,
  "aud": "dev",
  "refresh_jti": "uuid",
  "type": "access",
  "exp": 1234567890,
  "iat": 1234567890,
  "iss": "localhost",
  "jti": "uuid"
}
```

#### Refresh Token
```json
{
  "sub": "user@example.com",
  "exp": 1234567890,
  "iat": 1234567890,
  "jti": "uuid"
}
```

### Security Flow

1. **Login**: User provides credentials
2. **Validation**: Password verified with bcrypt
3. **Token Generation**: Access + Refresh tokens created
4. **Token Storage**: Refresh token hash stored in database
5. **Authentication**: Access token validated on each request
6. **Token Refresh**: New access token issued using refresh token
7. **Logout**: Refresh token revoked from database

### Security Features

- **Password Hashing**: bcrypt with configurable rounds
- **Timing Attack Prevention**: Dummy hash for non-existent users
- **Token Revocation**: Database-backed refresh token management
- **User Agent Tracking**: Detect token theft
- **IP Address Tracking**: Additional security layer
- **Symmetric Encryption**: ShieldCipher for sensitive data

## Dependency Injection

FastAPI's dependency injection system is used throughout:

### Database Session
```python
def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
```

### Authentication
```python
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    # Validate token and return user
```

### Service Injection
```python
def get_seccion_service(
    db: Session = Depends(get_db)
) -> SeccionService:
    return SeccionService(
        seccion_repository=SeccionRepository(db),
        # ... other dependencies
    )
```

## SIIAU Integration

### Task Service Architecture

The `TaskService` handles integration with the external SIIAU system:

1. **HTTP Request**: Fetch data from SIIAU endpoint
2. **HTML Parsing**: BeautifulSoup extracts table data
3. **Data Transformation**: Convert to internal schemas
4. **Validation**: Ensure data integrity
5. **Batch Processing**: Create multiple entities
6. **Error Handling**: Track and report errors
7. **Statistics**: Return creation counts

### Data Import Flow

```
SIIAU System
    ↓ (HTTP POST)
HTML Response
    ↓ (BeautifulSoup)
Parsed Table Data
    ↓ (Transformation)
SeccionSiiau Schema
    ↓ (Validation)
Service Layer
    ↓ (Batch Create)
Database
    ↓
Statistics Response
```

## Error Handling

### Custom Exceptions

- `UnauthorizedException` (401): Authentication failures
- `ForbiddenException` (403): Authorization failures
- `NotFoundException` (404): Resource not found
- `ConflictException` (409): Duplicate or conflict errors
- `BadRequestException` (400): Validation errors

### Exception Flow

```python
try:
    # Business logic
except CustomException as e:
    # Automatically converted to HTTP response
    raise HTTPException(status_code=e.status_code, detail=e.message)
```

## Pagination

### Implementation

All list endpoints support pagination:

```python
class PaginationParams:
    page: int = 1
    page_size: int = 10
```

### Response Format

```json
{
  "items": [...],
  "total": 100,
  "page": 1,
  "page_size": 10,
  "pages": 10
}
```

## Configuration Management

### Environment-Based Configuration

- **Development**: Debug mode, auto-seeding, SQLite
- **Production**: Optimized settings, PostgreSQL/MySQL

### Configuration Loading

1. Load `.env` file
2. Parse environment variables
3. Type conversion and validation
4. Create Settings singleton
5. Access via `settings` object

## Performance Considerations

### Database Optimization

- **Indexes**: Applied to frequently queried fields
- **Relationships**: Lazy loading by default
- **Connection Pooling**: Managed by SQLAlchemy
- **Query Optimization**: Repository pattern enables query tuning

### Caching Strategy

Currently not implemented, but architecture supports:
- Redis for session storage
- Query result caching
- Token blacklist caching

## Scalability

### Horizontal Scaling

- **Stateless API**: No server-side sessions
- **Database-backed tokens**: Shared state in database
- **Load Balancer Ready**: No sticky sessions required

### Vertical Scaling

- **Async Support**: FastAPI's async capabilities
- **Connection Pooling**: Database connection management
- **Resource Optimization**: Efficient query patterns

## Testing Strategy

### Unit Tests
- Service layer business logic
- Repository CRUD operations
- Utility functions

### Integration Tests
- API endpoint testing
- Database operations
- Authentication flow

### End-to-End Tests
- Complete user workflows
- SIIAU integration
- Multi-module operations

## Deployment Architecture

### Recommended Setup

```
Load Balancer
    ↓
Multiple API Instances (FastAPI)
    ↓
Database (PostgreSQL/MySQL)
    ↓
Redis (Optional - Caching)
```

### Container Deployment

```dockerfile
# Example Dockerfile structure
FROM python:3.10
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app/ ./app/
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0"]
```

## Monitoring & Logging

### Logging Strategy

- **Application Logs**: FastAPI request/response logging
- **Database Logs**: SQLAlchemy query logging (debug mode)
- **Error Logs**: Exception tracking
- **Access Logs**: Authentication attempts

### Metrics to Monitor

- Request rate and latency
- Database connection pool usage
- Authentication success/failure rate
- SIIAU integration success rate
- Error rates by endpoint

## Security Best Practices

1. **Environment Variables**: Never commit secrets
2. **HTTPS Only**: Enforce in production
3. **CORS Configuration**: Restrict allowed origins
4. **Rate Limiting**: Implement for production
5. **Input Validation**: All inputs validated via Pydantic
6. **SQL Injection Prevention**: ORM-based queries
7. **XSS Prevention**: JSON responses only
8. **Token Expiration**: Short-lived access tokens

## Future Enhancements

### Planned Features

- [ ] Alembic database migrations
- [ ] Redis caching layer
- [ ] WebSocket support for real-time updates
- [ ] GraphQL API option
- [ ] Advanced search and filtering
- [ ] Audit logging
- [ ] Rate limiting
- [ ] API versioning
- [ ] Comprehensive test suite
- [ ] CI/CD pipeline

### Architecture Improvements

- [ ] Event-driven architecture for async operations
- [ ] CQRS pattern for read/write separation
- [ ] Microservices decomposition (if needed)
- [ ] Message queue for background tasks
- [ ] Service mesh for inter-service communication

## Conclusion

SIIAPI's architecture prioritizes:
- **Maintainability**: Clear separation of concerns
- **Scalability**: Stateless design, horizontal scaling ready
- **Security**: Multiple layers of protection
- **Testability**: Dependency injection, layered architecture
- **Extensibility**: Modular design, easy to add features

The architecture supports both current requirements and future growth while maintaining code quality and developer productivity.