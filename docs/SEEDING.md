# Database Seeding

Este documento explica cómo poblar la base de datos con datos iniciales (seed data) en diferentes entornos.

## Descripción General

El proyecto incluye un sistema de seeding que crea datos iniciales necesarios para el funcionamiento de la aplicación, como el usuario administrador por defecto.

## Comportamiento por Entorno

### Modo Desarrollo (`APP_DEBUG=True`)

En desarrollo, el seed data se ejecuta **automáticamente** al iniciar la aplicación:

```bash
# En tu archivo .env
APP_DEBUG=True

# Al iniciar la aplicación
uvicorn app.main:app --reload
```

Esto ejecutará:
1. `init_db()` - Crea todas las tablas
2. `seed_data()` - Inserta datos iniciales

### Modo Producción (`APP_DEBUG=False`)

En producción, tienes **3 opciones** para ejecutar el seed data:

#### Opción 1: Seed Automático en Startup (Recomendado para primer despliegue)

Configura la variable de entorno `DB_SEED_ON_STARTUP=True`:

```bash
# En tu archivo .env
APP_DEBUG=False
DB_SEED_ON_STARTUP=True

# Al iniciar la aplicación
uvicorn app.main:app
```

Esto ejecutará:
1. Migraciones de Alembic
2. Seed data automáticamente

**⚠️ Advertencia:** Desactiva `DB_SEED_ON_STARTUP` después del primer despliegue para evitar intentos de crear datos duplicados en cada reinicio.

#### Opción 2: Seed Manual con Makefile (Recomendado)

Ejecuta el seed manualmente cuando lo necesites:

```bash
make db-seed
```

Este comando ejecuta el script `scripts/seed_database.py` que:
- Verifica si ya existen datos
- Inserta solo los datos necesarios
- Muestra mensajes de éxito/error

#### Opción 3: Seed Manual con Python

Ejecuta directamente el script de Python:

```bash
python scripts/seed_database.py
```

O desde código Python:

```python
from app.core.seed import seed_data

seed_data()
```

## Datos que se Crean

El seed actual crea:

### Usuario Administrador

```python
{
    "name": "Admin",
    "email": "admin@example.com",
    "password": "admin",
    "is_active": True,
    "is_superuser": True,
    "credits": 100
}
```

**🔒 Importante:** Cambia la contraseña del administrador inmediatamente después del primer login en producción.

## Personalizar Seed Data

### Agregar Nuevos Datos

Edita `app/core/seed.py`:

```python
from app.api.dependencies.database import get_session
from app.modules.users.api.dependencies import get_user_service
from app.modules.users.schemas import UserCreate


def seed_data():
    session = next(get_session())
    create_superuser(session)
    create_default_categories(session)  # Nueva función
    create_sample_data(session)  # Nueva función


def create_superuser(session):
    service = get_user_service(session)
    _, total = service.list_users()

    if not total:
        service.create_user(
            UserCreate(
                name="Admin",
                email="admin@example.com",
                password="admin",
                is_active=True,
                is_superuser=True,
                credits=100,
            )
        )


def create_default_categories(session):
    # Tu código aquí
    pass


def create_sample_data(session):
    # Tu código aquí
    pass
```

### Seed Condicional

Puedes hacer que ciertos datos solo se creen en desarrollo:

```python
from app.core.config import settings

def seed_data():
    session = next(get_session())
    create_superuser(session)
    
    # Solo en desarrollo
    if settings.APP_DEBUG:
        create_sample_data(session)
```

## Flujos de Trabajo Comunes

### Primer Despliegue en Producción

```bash
# 1. Configurar variables de entorno
APP_DEBUG=False
DB_SEED_ON_STARTUP=True

# 2. Iniciar aplicación (ejecuta migraciones + seed)
uvicorn app.main:app

# 3. Verificar que todo funciona
curl http://localhost:8000/api/health

# 4. Desactivar seed automático
DB_SEED_ON_STARTUP=False

# 5. Reiniciar aplicación
```

### Desarrollo Local

```bash
# 1. Configurar modo debug
APP_DEBUG=True

# 2. Iniciar aplicación (crea tablas + seed automático)
uvicorn app.main:app --reload

# 3. Si necesitas resetear datos
rm db.sqlite3
# Reiniciar aplicación
```

### Agregar Datos Adicionales en Producción

```bash
# Opción A: Ejecutar seed manualmente
make db-seed

# Opción B: Usar script Python
python scripts/seed_database.py

# Opción C: Crear migración de datos con Alembic
alembic revision -m "Add default categories"
# Editar el archivo de migración para insertar datos
alembic upgrade head
```

## Mejores Prácticas

### ✅ DO

- **Verificar antes de insertar**: Siempre verifica si los datos ya existen antes de insertarlos
- **Usar transacciones**: Envuelve operaciones de seed en transacciones
- **Logging**: Registra qué datos se están creando
- **Idempotencia**: El seed debe poder ejecutarse múltiples veces sin errores
- **Datos mínimos**: Solo crea datos absolutamente necesarios
- **Documentar**: Documenta qué datos crea cada función de seed

### ❌ DON'T

- **No hardcodear contraseñas**: Usa variables de entorno para credenciales sensibles
- **No crear datos masivos**: El seed es para datos iniciales, no para datos de prueba masivos
- **No ejecutar en cada startup**: En producción, ejecuta seed solo cuando sea necesario
- **No ignorar errores**: Maneja errores apropiadamente y registra fallos

## Troubleshooting

### Error: "Duplicate entry"

El seed está intentando crear datos que ya existen. Soluciones:

```python
# Verificar antes de crear
def create_superuser(session):
    service = get_user_service(session)
    _, total = service.list_users()
    
    if not total:  # Solo crear si no hay usuarios
        service.create_user(...)
```

### Error: "Foreign key constraint"

Estás intentando crear datos que dependen de otros datos que no existen. Solución:

```python
def seed_data():
    session = next(get_session())
    # Orden correcto: primero las dependencias
    create_categories(session)  # Primero
    create_products(session)    # Después (depende de categories)
```

### Seed no se ejecuta en producción

Verifica:

1. `APP_DEBUG=False` está configurado
2. `DB_SEED_ON_STARTUP=True` está configurado (si quieres seed automático)
3. Las migraciones se ejecutaron correctamente
4. Revisa los logs de la aplicación

### Necesito resetear la base de datos

**Desarrollo:**
```bash
rm db.sqlite3
uvicorn app.main:app --reload
```

**Producción (⚠️ CUIDADO - Perderás todos los datos):**
```bash
# 1. Backup de la base de datos
cp production.db production.db.backup

# 2. Eliminar base de datos
rm production.db

# 3. Ejecutar migraciones
alembic upgrade head

# 4. Ejecutar seed
make db-seed
```

## Ejemplos Avanzados

### Seed con Datos de Archivo

```python
import json
from pathlib import Path

def seed_from_file(session, filename):
    """Cargar datos desde un archivo JSON."""
    file_path = Path(__file__).parent / "seed_data" / filename
    
    with open(file_path) as f:
        data = json.load(f)
    
    # Procesar y crear datos
    for item in data:
        # Tu lógica aquí
        pass
```

### Seed con Progreso

```python
from tqdm import tqdm

def seed_large_dataset(session):
    """Seed con barra de progreso para datasets grandes."""
    items = [...]  # Lista de items a crear
    
    for item in tqdm(items, desc="Seeding data"):
        # Crear item
        pass
```

### Seed Condicional por Entorno

```python
import os

def seed_data():
    session = next(get_session())
    
    # Siempre crear admin
    create_superuser(session)
    
    # Solo en staging/development
    if os.getenv("APP_ENV") in ["dev", "staging"]:
        create_test_users(session)
        create_sample_data(session)
    
    # Solo en producción
    if os.getenv("APP_ENV") == "production":
        create_production_defaults(session)
```

## Referencias

- Código de seed: `app/core/seed.py`
- Script de seed: `scripts/seed_database.py`
- Configuración: `app/core/config.py`
- Makefile: `Makefile` (comando `make db-seed`)