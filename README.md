# SIIAPI

A FastAPI-based REST API for managing university academic information, including courses, sections, professors, classrooms, and schedules. This system integrates with SIIAU (Sistema Integral de Información Académica Universitaria) to fetch and manage academic data.

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [Database Models](#database-models)
- [Authentication](#authentication)
- [Development](#development)
- [License](#license)

## ✨ Features

- **User Management**: User registration, authentication, and authorization
- **JWT Authentication**: Secure token-based authentication with refresh tokens
- **Academic Calendar Management**: Manage academic calendars and periods
- **University Centers**: Manage university centers (centros universitarios)
- **Course Management**: Create and manage courses (materias) with credits and codes
- **Section Management**: Handle course sections with enrollment capacity
- **Professor Management**: Manage professor information
- **Building & Classroom Management**: Track buildings (edificios) and classrooms (aulas)
- **Class Scheduling**: Manage class schedules with time slots and days
- **SIIAU Integration**: Fetch and import data from SIIAU system
- **Pagination Support**: Built-in pagination for list endpoints
- **Data Seeding**: Automatic database seeding in development mode

## 🛠 Tech Stack

- **Framework**: FastAPI
- **Database ORM**: SQLModel (SQLAlchemy + Pydantic)
- **Authentication**: JWT (python-jose) with bcrypt password hashing
- **Encryption**: ShieldCipher for symmetric encryption
- **Web Scraping**: BeautifulSoup4 and Requests for SIIAU integration
- **Python Version**: 3.10+

## 📁 Project Structure

```
SIIAPI/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── api/
│   │   ├── routes.py           # Main API router
│   │   ├── dependencies/       # Shared dependencies
│   │   └── schemas/            # Shared schemas (pagination)
│   ├── core/
│   │   ├── config.py           # Application configuration
│   │   ├── database.py         # Database setup and initialization
│   │   ├── security.py         # Security utilities (JWT, hashing, encryption)
│   │   ├── exceptions.py       # Custom exceptions
│   │   └── seed.py             # Database seeding
│   └── modules/
│       ├── auth/               # Authentication module
│       ├── users/              # User management
│       ├── calendario/         # Academic calendar
│       ├── centro/             # University centers
│       ├── materia/            # Courses/subjects
│       ├── seccion/            # Course sections
│       ├── profesor/           # Professors
│       ├── clase/              # Class schedules
│       ├── edificio/           # Buildings
│       ├── aula/               # Classrooms
│       └── tasks/              # SIIAU integration tasks
├── requirements.txt
├── dev.sh                      # Development script
└── LICENSE
```

### Module Structure

Each module follows a consistent architecture:

```
module_name/
├── __init__.py
├── api/
│   ├── dependencies.py         # Module-specific dependencies
│   └── routes.py               # API endpoints
├── models/
│   └── model_name.py           # SQLModel database models
├── repositories/
│   └── repository.py           # Data access layer
├── schemas/
│   └── schema.py               # Pydantic schemas for validation
└── services/
    └── service.py              # Business logic layer
```

## 🚀 Installation

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)

### Steps

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd SIIAPI
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## ⚙️ Configuration

Create a `.env` file in the root directory with the following variables:

```env
# Database
DB_URL=sqlite:///./db.sqlite3
# For PostgreSQL: postgresql://user:password@localhost/dbname
# For MySQL: mysql://user:password@localhost/dbname

# Application
APP_NAME=SIIAPI
APP_SITE=localhost
APP_ENV=dev
APP_DESCRIPTION=University Academic Information API
APP_DEBUG=true

# Security
SECRET_KEY=your-secret-key-here-change-in-production
DUMMY_HASH=$2b$12$your-dummy-hash-for-timing-attack-prevention

# SIIAU Integration
SIIAU_URL=https://siiau.udg.mx/wco/sspseca.consulta_oferta
```

### Configuration Options

- **DB_URL**: Database connection string (supports SQLite, PostgreSQL, MySQL)
- **APP_DEBUG**: Enable debug mode (auto-creates tables and seeds data)
- **SECRET_KEY**: Secret key for JWT token generation (change in production!)
- **DUMMY_HASH**: Bcrypt hash used for timing attack prevention
- **SIIAU_URL**: URL endpoint for SIIAU data fetching

## 🏃 Running the Application

### Development Mode

Using the provided script:
```bash
chmod +x dev.sh
./dev.sh
```

Or manually:
```bash
fastapi dev app/main.py
```

The API will be available at `http://localhost:8000`

### Production Mode

```bash
fastapi run app/main.py
```

Or with Uvicorn:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## 📚 API Documentation

Once the application is running, access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Main API Endpoints

#### Authentication
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout
- `POST /api/auth/refresh` - Refresh access token

#### Users
- `GET /api/users` - List users (paginated)
- `POST /api/users` - Create user
- `GET /api/users/{id}` - Get user by ID
- `PUT /api/users/{id}` - Update user
- `DELETE /api/users/{id}` - Delete user

#### Calendarios (Academic Calendars)
- `GET /api/calendarios` - List calendars
- `POST /api/calendarios` - Create calendar
- `GET /api/calendarios/{id}` - Get calendar
- `PUT /api/calendarios/{id}` - Update calendar
- `DELETE /api/calendarios/{id}` - Delete calendar

#### Centros (University Centers)
- `GET /api/centros` - List centers
- `POST /api/centros` - Create center
- `GET /api/centros/{id}` - Get center
- `PUT /api/centros/{id}` - Update center
- `DELETE /api/centros/{id}` - Delete center

#### Materias (Courses)
- `GET /api/materias` - List courses
- `POST /api/materias` - Create course
- `GET /api/materias/{id}` - Get course
- `PUT /api/materias/{id}` - Update course
- `DELETE /api/materias/{id}` - Delete course

#### Secciones (Course Sections)
- `GET /api/secciones` - List sections
- `POST /api/secciones` - Create section
- `GET /api/secciones/{id}` - Get section
- `PUT /api/secciones/{id}` - Update section
- `DELETE /api/secciones/{id}` - Delete section

#### Profesores (Professors)
- `GET /api/profesores` - List professors
- `POST /api/profesores` - Create professor
- `GET /api/profesores/{id}` - Get professor
- `PUT /api/profesores/{id}` - Update professor
- `DELETE /api/profesores/{id}` - Delete professor

#### Clases (Class Schedules)
- `GET /api/clases` - List classes
- `POST /api/clases` - Create class
- `GET /api/clases/{id}` - Get class
- `PUT /api/clases/{id}` - Update class
- `DELETE /api/clases/{id}` - Delete class

#### Edificios (Buildings)
- `GET /api/edificios` - List buildings
- `POST /api/edificios` - Create building
- `GET /api/edificios/{id}` - Get building
- `PUT /api/edificios/{id}` - Update building
- `DELETE /api/edificios/{id}` - Delete building

#### Aulas (Classrooms)
- `GET /api/aulas` - List classrooms
- `POST /api/aulas` - Create classroom
- `GET /api/aulas/{id}` - Get classroom
- `PUT /api/aulas/{id}` - Update classroom
- `DELETE /api/aulas/{id}` - Delete classroom

#### Tasks (SIIAU Integration)
- `POST /api/tasks/fetch-secciones` - Fetch sections from SIIAU

## 🗄️ Database Models

### User
- User accounts with authentication
- Fields: name, email, password, is_active, is_superuser, is_staff
- Tracks: created_at, updated_at, last_login

### RefreshToken
- JWT refresh tokens for authentication
- Tracks: token_hash, jti, user_agent, ip_address, expires_at

### Calendario
- Academic calendar periods
- Fields: name, siiau_id

### CentroUniversitario
- University centers/campuses
- Fields: name, siiau_id

### Materia
- Academic courses/subjects
- Fields: name, clave (code), creditos (credits)

### Profesor
- Professor information
- Fields: name

### Seccion
- Course sections with enrollment
- Fields: name, nrc, cupos, cupos_disponibles, periodo_inicio, periodo_fin
- Relations: centro, materia, profesor, calendario

### Clase
- Individual class sessions
- Fields: sesion, hora_inicio, hora_fin, dia (day of week)
- Relations: seccion, aula

### Edificio
- Building information
- Fields: name
- Relations: centro

### Aula
- Classroom information
- Fields: name
- Relations: edificio

## 🔐 Authentication

The API uses JWT (JSON Web Tokens) for authentication with a dual-token system:

### Access Tokens
- Short-lived tokens for API requests
- Include user permissions (is_superuser, is_staff)
- Expire after 1 day

### Refresh Tokens
- Long-lived tokens for obtaining new access tokens
- Stored in database with metadata (user_agent, ip_address)
- Can be revoked individually
- Expire after 1 day (configurable)

### Security Features
- Password hashing with bcrypt
- Timing attack prevention with dummy hash
- Token revocation support
- User agent and IP tracking
- Symmetric encryption with ShieldCipher

### Authentication Flow

1. **Login**: POST credentials to `/api/auth/login`
   - Returns access_token and refresh_token
   
2. **Authenticated Requests**: Include access token in header
   ```
   Authorization: Bearer <access_token>
   ```

3. **Token Refresh**: POST refresh_token to `/api/auth/refresh`
   - Returns new access_token

4. **Logout**: POST refresh_token to `/api/auth/logout`
   - Revokes the refresh token

## 👨‍💻 Development

### Code Organization

The project follows a modular architecture with clear separation of concerns:

- **Models**: Database schema definitions using SQLModel
- **Schemas**: Request/response validation using Pydantic
- **Repositories**: Data access layer (CRUD operations)
- **Services**: Business logic layer
- **API Routes**: HTTP endpoint definitions
- **Dependencies**: Dependency injection for database sessions and authentication

### Adding a New Module

1. Create module directory structure:
   ```bash
   mkdir -p app/modules/new_module/{api,models,repositories,schemas,services}
   ```

2. Create model in `models/new_model.py`
3. Create schemas in `schemas/new_schema.py`
4. Create repository in `repositories/new_repository.py`
5. Create service in `services/new_service.py`
6. Create routes in `api/routes.py`
7. Register routes in `app/api/routes.py`
8. Import model in `app/core/database.py`

### Database Migrations

Currently using SQLModel's `create_all()` for table creation. For production, consider using Alembic for migrations.

### Testing

The project structure supports easy testing:
- Unit tests for services
- Integration tests for repositories
- API tests for routes

## 📄 License

This project is licensed under the GNU Affero General Public License v3.0 (AGPL-3.0).

See the [LICENSE](LICENSE) file for details.

### Key Points of AGPL-3.0:
- Free to use, modify, and distribute
- Must disclose source code when distributing
- Network use is considered distribution (must provide source to users)
- Modifications must be released under AGPL-3.0
- No warranty provided

## 🤝 Contributing

Contributions are welcome! Please ensure:
- Code follows the existing architecture patterns
- All endpoints include proper authentication/authorization
- Database models include proper relationships and constraints
- API responses use appropriate schemas

## 📞 Support

For issues, questions, or contributions, please open an issue in the repository.

---

**Note**: This is an academic project for managing university course information. Ensure proper configuration and security measures before deploying to production.