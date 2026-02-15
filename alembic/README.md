# Alembic Database Migrations

This directory contains Alembic database migration scripts for the SIIAPI project.

## Overview

Alembic is used for database schema migrations in production environments. The application automatically runs migrations when `APP_DEBUG=False`.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Ensure your `.env` file has the correct `DB_URL` configured.

## Creating Migrations

### Auto-generate a migration (recommended)

Alembic can automatically detect changes in your SQLModel models and generate migration scripts:

```bash
alembic revision --autogenerate -m "Description of changes"
```

This will:
- Compare your SQLModel models with the current database schema
- Generate a new migration file in `alembic/versions/`
- Include upgrade() and downgrade() functions

**Important:** Always review auto-generated migrations before applying them!

### Create an empty migration

If you need to write a custom migration:

```bash
alembic revision -m "Description of changes"
```

## Running Migrations

### Automatic (Production)

When `APP_DEBUG=False`, migrations run automatically on application startup via `app/core/migrations.py`.

### Manual

Upgrade to the latest version:
```bash
alembic upgrade head
```

Upgrade to a specific revision:
```bash
alembic upgrade <revision_id>
```

Downgrade one revision:
```bash
alembic downgrade -1
```

Downgrade to a specific revision:
```bash
alembic downgrade <revision_id>
```

## Viewing Migration History

Show current revision:
```bash
alembic current
```

Show migration history:
```bash
alembic history
```

Show migration history with details:
```bash
alembic history --verbose
```

## Development vs Production

### Development Mode (APP_DEBUG=True)
- Uses `SQLModel.metadata.create_all()` for quick schema creation
- Runs seed data automatically
- No migrations are applied
- Suitable for rapid development and testing

### Production Mode (APP_DEBUG=False)
- Uses Alembic migrations for controlled schema changes
- Migrations run automatically on startup
- No seed data is run
- Provides version control for database schema

## Best Practices

1. **Always review auto-generated migrations** - Alembic may not detect all changes correctly
2. **Test migrations** - Test both upgrade and downgrade paths
3. **One logical change per migration** - Keep migrations focused and atomic
4. **Add comments** - Document complex migrations
5. **Never edit applied migrations** - Create a new migration to fix issues
6. **Backup before migrating** - Always backup production databases before running migrations

## Troubleshooting

### Migration fails with "target database is not up to date"
```bash
alembic stamp head
```

### Reset migrations (development only)
```bash
# Delete the database
rm db.sqlite3

# Delete all migration files (keep __init__.py)
rm alembic/versions/*.py

# Create initial migration
alembic revision --autogenerate -m "Initial migration"

# Apply migration
alembic upgrade head
```

## File Structure

```
alembic/
├── README.md           # This file
├── env.py             # Alembic environment configuration
├── script.py.mako     # Template for new migrations
└── versions/          # Migration scripts directory
    └── *.py           # Individual migration files
```

## Additional Resources

- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)