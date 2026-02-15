# API Documentation

## Base URL

```
http://localhost:8000/api
```

## Authentication

Most endpoints require authentication using JWT Bearer tokens.

### Headers

```http
Authorization: Bearer <access_token>
Content-Type: application/json
```

## Response Format

### Success Response

```json
{
  "id": 1,
  "name": "Example",
  "created_at": "2024-01-01T00:00:00"
}
```

### Error Response

```json
{
  "detail": "Error message"
}
```

### Paginated Response

```json
{
  "items": [...],
  "total": 100,
  "page": 1,
  "page_size": 10,
  "pages": 10
}
```

## Authentication Endpoints

### Login

Authenticate user and receive access and refresh tokens.

**Endpoint**: `POST /api/auth/login`

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "password123",
  "remember_me": false,
  "audience": "dev",
  "user_agent": "Mozilla/5.0...",
  "ip_address": "192.168.1.1"
}
```

**Response**: `200 OK`
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "access_token_expires_at": 1234567890,
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token_expires_at": 1234567890
}
```

**Errors**:
- `400 Bad Request`: Invalid credentials
- `403 Forbidden`: User is inactive

---

### Refresh Token

Get a new access token using a refresh token.

**Endpoint**: `POST /api/auth/refresh`

**Request Body**:
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "audience": "dev",
  "user_agent": "Mozilla/5.0...",
  "ip_address": "192.168.1.1"
}
```

**Response**: `200 OK`
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "access_token_expires_at": 1234567890,
  "refresh_token": null,
  "refresh_token_expires_at": null
}
```

**Errors**:
- `401 Unauthorized`: Invalid or expired refresh token

---

### Logout

Revoke a refresh token.

**Endpoint**: `POST /api/auth/logout`

**Authentication**: Required

**Request Body**:
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user_agent": "Mozilla/5.0...",
  "ip_address": "192.168.1.1"
}
```

**Response**: `204 No Content`

**Errors**:
- `401 Unauthorized`: Invalid refresh token

---

## User Endpoints

### List Users

Get a paginated list of users.

**Endpoint**: `GET /api/users`

**Authentication**: Required

**Query Parameters**:
- `page` (integer, default: 1): Page number
- `page_size` (integer, default: 10): Items per page
- `email` (string, optional): Filter by email
- `name` (string, optional): Filter by name
- `is_active` (boolean, optional): Filter by active status

**Response**: `200 OK`
```json
{
  "items": [
    {
      "id": 1,
      "name": "John Doe",
      "email": "john@example.com",
      "is_active": true,
      "is_superuser": false,
      "is_staff": false,
      "created_at": "2024-01-01T00:00:00",
      "updated_at": "2024-01-01T00:00:00",
      "last_login": "2024-01-01T00:00:00"
    }
  ],
  "total": 1,
  "page": 1,
  "page_size": 10,
  "pages": 1
}
```

---

### Create User

Create a new user.

**Endpoint**: `POST /api/users`

**Authentication**: Required (Admin)

**Request Body**:
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "securepassword123",
  "is_active": true,
  "is_superuser": false,
  "is_staff": false
}
```

**Response**: `201 Created`
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "is_active": true,
  "is_superuser": false,
  "is_staff": false,
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00",
  "last_login": null
}
```

**Errors**:
- `409 Conflict`: Email already exists

---

### Get User

Get a specific user by ID.

**Endpoint**: `GET /api/users/{id}`

**Authentication**: Required

**Response**: `200 OK`
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "is_active": true,
  "is_superuser": false,
  "is_staff": false,
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00",
  "last_login": "2024-01-01T00:00:00"
}
```

**Errors**:
- `404 Not Found`: User not found

---

### Update User

Update a user.

**Endpoint**: `PUT /api/users/{id}`

**Authentication**: Required (Admin or Self)

**Request Body**:
```json
{
  "name": "John Updated",
  "email": "john.updated@example.com",
  "is_active": true
}
```

**Response**: `200 OK`
```json
{
  "id": 1,
  "name": "John Updated",
  "email": "john.updated@example.com",
  "is_active": true,
  "is_superuser": false,
  "is_staff": false,
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-02T00:00:00",
  "last_login": "2024-01-01T00:00:00"
}
```

---

### Delete User

Delete a user.

**Endpoint**: `DELETE /api/users/{id}`

**Authentication**: Required (Admin)

**Response**: `204 No Content`

**Errors**:
- `404 Not Found`: User not found

---

## Calendario Endpoints

### List Calendarios

Get a paginated list of academic calendars.

**Endpoint**: `GET /api/calendarios`

**Query Parameters**:
- `page` (integer, default: 1)
- `page_size` (integer, default: 10)
- `name` (string, optional): Filter by name
- `siiau_id` (string, optional): Filter by SIIAU ID

**Response**: `200 OK`
```json
{
  "items": [
    {
      "id": 1,
      "name": "2024A",
      "siiau_id": "202410"
    }
  ],
  "total": 1,
  "page": 1,
  "page_size": 10,
  "pages": 1
}
```

---

### Create Calendario

**Endpoint**: `POST /api/calendarios`

**Authentication**: Required (Admin)

**Request Body**:
```json
{
  "name": "2024A",
  "siiau_id": "202410"
}
```

**Response**: `201 Created`

---

### Get Calendario

**Endpoint**: `GET /api/calendarios/{id}`

**Response**: `200 OK`

---

### Update Calendario

**Endpoint**: `PUT /api/calendarios/{id}`

**Authentication**: Required (Admin)

---

### Delete Calendario

**Endpoint**: `DELETE /api/calendarios/{id}`

**Authentication**: Required (Admin)

**Response**: `204 No Content`

---

## Centro Endpoints

### List Centros

Get a paginated list of university centers.

**Endpoint**: `GET /api/centros`

**Query Parameters**:
- `page` (integer, default: 1)
- `page_size` (integer, default: 10)
- `name` (string, optional): Filter by name
- `siiau_id` (string, optional): Filter by SIIAU ID

**Response**: `200 OK`
```json
{
  "items": [
    {
      "id": 1,
      "name": "CUCEI",
      "siiau_id": "D"
    }
  ],
  "total": 1,
  "page": 1,
  "page_size": 10,
  "pages": 1
}
```

---

### Create Centro

**Endpoint**: `POST /api/centros`

**Authentication**: Required (Admin)

**Request Body**:
```json
{
  "name": "CUCEI",
  "siiau_id": "D"
}
```

**Response**: `201 Created`

---

## Materia Endpoints

### List Materias

Get a paginated list of courses.

**Endpoint**: `GET /api/materias`

**Query Parameters**:
- `page` (integer, default: 1)
- `page_size` (integer, default: 10)
- `name` (string, optional): Filter by name
- `clave` (string, optional): Filter by course code
- `creditos` (integer, optional): Filter by credits

**Response**: `200 OK`
```json
{
  "items": [
    {
      "id": 1,
      "name": "Programación Orientada a Objetos",
      "clave": "I5883",
      "creditos": 8
    }
  ],
  "total": 1,
  "page": 1,
  "page_size": 10,
  "pages": 1
}
```

---

### Create Materia

**Endpoint**: `POST /api/materias`

**Authentication**: Required (Admin)

**Request Body**:
```json
{
  "name": "Programación Orientada a Objetos",
  "clave": "I5883",
  "creditos": 8
}
```

**Response**: `201 Created`

**Errors**:
- `409 Conflict`: Course code (clave) already exists

---

## Profesor Endpoints

### List Profesores

Get a paginated list of professors.

**Endpoint**: `GET /api/profesores`

**Query Parameters**:
- `page` (integer, default: 1)
- `page_size` (integer, default: 10)
- `name` (string, optional): Filter by name

**Response**: `200 OK`
```json
{
  "items": [
    {
      "id": 1,
      "name": "GARCIA LOPEZ JUAN CARLOS"
    }
  ],
  "total": 1,
  "page": 1,
  "page_size": 10,
  "pages": 1
}
```

---

### Create Profesor

**Endpoint**: `POST /api/profesores`

**Authentication**: Required (Admin)

**Request Body**:
```json
{
  "name": "GARCIA LOPEZ JUAN CARLOS"
}
```

**Response**: `201 Created`

---

## Seccion Endpoints

### List Secciones

Get a paginated list of course sections.

**Endpoint**: `GET /api/secciones`

**Query Parameters**:
- `page` (integer, default: 1)
- `page_size` (integer, default: 10)
- `nrc` (string, optional): Filter by NRC
- `centro_id` (integer, optional): Filter by center
- `materia_id` (integer, optional): Filter by course
- `profesor_id` (integer, optional): Filter by professor
- `calendario_id` (integer, optional): Filter by calendar

**Response**: `200 OK`
```json
{
  "items": [
    {
      "id": 1,
      "name": "D01",
      "nrc": "12345",
      "cupos": 30,
      "cupos_disponibles": 15,
      "periodo_inicio": "2024-01-15T00:00:00",
      "periodo_fin": "2024-06-15T00:00:00",
      "centro_id": 1,
      "materia_id": 1,
      "profesor_id": 1,
      "calendario_id": 1
    }
  ],
  "total": 1,
  "page": 1,
  "page_size": 10,
  "pages": 1
}
```

---

### Create Seccion

**Endpoint**: `POST /api/secciones`

**Authentication**: Required (Admin)

**Request Body**:
```json
{
  "name": "D01",
  "nrc": "12345",
  "cupos": 30,
  "cupos_disponibles": 30,
  "periodo_inicio": "2024-01-15T00:00:00",
  "periodo_fin": "2024-06-15T00:00:00",
  "centro_id": 1,
  "materia_id": 1,
  "profesor_id": 1,
  "calendario_id": 1
}
```

**Response**: `201 Created`

---

## Clase Endpoints

### List Clases

Get a paginated list of class schedules.

**Endpoint**: `GET /api/clases`

**Query Parameters**:
- `page` (integer, default: 1)
- `page_size` (integer, default: 10)
- `seccion_id` (integer, optional): Filter by section
- `aula_id` (integer, optional): Filter by classroom
- `dia` (integer, optional): Filter by day (1-7)

**Response**: `200 OK`
```json
{
  "items": [
    {
      "id": 1,
      "sesion": 1,
      "hora_inicio": "07:00:00",
      "hora_fin": "08:50:00",
      "dia": 1,
      "seccion_id": 1,
      "aula_id": 1
    }
  ],
  "total": 1,
  "page": 1,
  "page_size": 10,
  "pages": 1
}
```

**Note**: `dia` represents day of week (1=Monday, 7=Sunday)

---

### Create Clase

**Endpoint**: `POST /api/clases`

**Authentication**: Required (Admin)

**Request Body**:
```json
{
  "sesion": 1,
  "hora_inicio": "07:00:00",
  "hora_fin": "08:50:00",
  "dia": 1,
  "seccion_id": 1,
  "aula_id": 1
}
```

**Response**: `201 Created`

---

## Edificio Endpoints

### List Edificios

Get a paginated list of buildings.

**Endpoint**: `GET /api/edificios`

**Query Parameters**:
- `page` (integer, default: 1)
- `page_size` (integer, default: 10)
- `name` (string, optional): Filter by name
- `centro_id` (integer, optional): Filter by center

**Response**: `200 OK`
```json
{
  "items": [
    {
      "id": 1,
      "name": "V",
      "centro_id": 1
    }
  ],
  "total": 1,
  "page": 1,
  "page_size": 10,
  "pages": 1
}
```

---

### Create Edificio

**Endpoint**: `POST /api/edificios`

**Authentication**: Required (Admin)

**Request Body**:
```json
{
  "name": "V",
  "centro_id": 1
}
```

**Response**: `201 Created`

---

## Aula Endpoints

### List Aulas

Get a paginated list of classrooms.

**Endpoint**: `GET /api/aulas`

**Query Parameters**:
- `page` (integer, default: 1)
- `page_size` (integer, default: 10)
- `name` (string, optional): Filter by name
- `edificio_id` (integer, optional): Filter by building

**Response**: `200 OK`
```json
{
  "items": [
    {
      "id": 1,
      "name": "101",
      "edificio_id": 1
    }
  ],
  "total": 1,
  "page": 1,
  "page_size": 10,
  "pages": 1
}
```

---

### Create Aula

**Endpoint**: `POST /api/aulas`

**Authentication**: Required (Admin)

**Request Body**:
```json
{
  "name": "101",
  "edificio_id": 1
}
```

**Response**: `201 Created`

---

## Task Endpoints

### Fetch Secciones from SIIAU

Fetch and import course sections from SIIAU system.

**Endpoint**: `POST /api/tasks/fetch-secciones`

**Authentication**: Required (Admin)

**Request Body**:
```json
{
  "calendario_id": 1,
  "centro_id": 1
}
```

**Response**: `200 OK`
```json
{
  "secciones_creadas": 150,
  "materias_creadas": 45,
  "profesores_creados": 30,
  "edificios_creados": 5,
  "aulas_creadas": 20,
  "clases_creadas": 300,
  "errores": 2
}
```

**Description**: This endpoint:
1. Fetches data from SIIAU for the specified calendar and center
2. Parses the HTML response
3. Creates or updates entities (materias, profesores, edificios, aulas)
4. Creates secciones and clases
5. Returns statistics about created entities

**Errors**:
- `404 Not Found`: Calendar or center not found
- `500 Internal Server Error`: SIIAU connection or parsing error

---

## HTTP Status Codes

- `200 OK`: Successful GET/PUT request
- `201 Created`: Successful POST request
- `204 No Content`: Successful DELETE request
- `400 Bad Request`: Invalid request data
- `401 Unauthorized`: Authentication required or failed
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `409 Conflict`: Resource conflict (duplicate)
- `500 Internal Server Error`: Server error

---

## Rate Limiting

Currently not implemented. Consider implementing rate limiting in production.

---

## Versioning

Current API version: v1 (implicit in `/api` prefix)

Future versions may use: `/api/v2/...`

---

## CORS

Configure CORS settings in production to restrict allowed origins.

---

## Interactive Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

These provide interactive API testing and comprehensive documentation.