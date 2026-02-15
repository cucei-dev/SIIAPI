# Database Migrations with Alembic

This document explains how database migrations are handled in the SIIAPI project using Alembic.

## Overview

The project uses **Alembic** for database schema migrations in production environments. The migration strategy differs based on the `APP_DEBUG` environment variable:

- **Development Mode** (`APP_DEBUG=True`): Uses SQLModel's `create_all()` for rapid development + automatic seed data
- **Production Mode** (`APP_DEBUG=False`): Uses Alembic migrations for controlled schema changes

> **📝 Note:** For information about seeding the database with initial data, see [SEEDING.md](./SEEDING.md)

## Architecture

### Key Files

```
├── alembic/
│   ├── env.py              # Alembic environment configuration
│   ├── script.py.mako      # Template for new migrations
│   ├── versions/           # Migration scripts directory
│   └── README.md           # Alembic-specific documentation
├── alembic.ini             # Alembic configuration file
├── app/
│   ├── core/
│   │   ├── migrations.py   # Migration utilities
│   │   └── database.py     # Database configuration
│   └── main.py             # Application entry point (runs migrations)
└── Makefile                # Convenient migration commands
```

### How It Works

1. **Startup Behavior** (`app/main.py`):
   ```python
   if settings.APP_DEBUG:
       # Development: Quick schema creation
       init_db()
       seed_data()
   else:
       # Production: Run migrations
       run_migrations()
   ```

2. **Migration Runner** (`app/core/migrations.py`):
   - Programmatically runs Alembic migrations
   - Automatically upgrades to the latest version
   - Logs migration progress and errors

3. **Alembic Configuration** (`alembic/env.py`):
   - Imports all SQLModel models
   - Uses `SQLModel.metadata` for autogeneration
   - Reads database URL from application settings

## Usage

### Creating Migrations

#### Auto-generate from model changes (recommended)

```bash
# Using Makefile
make migrate-create

# Or directly with Alembic
alembic revision --autogenerate -m "Add user email field"
```

This will:
1. Compare your SQLModel models with the current database schema
2. Generate a migration file in `alembic/versions/`
3. Include both `upgrade()` and `downgrade()` functions

**Important:** Always review auto-generated migrations before applying them!

#### Create empty migration for custom changes

```bash
alembic revision -m "Custom data migration"
```

### Running Migrations

#### Automatic (Production)

Migrations run automatically when the application starts with `APP_DEBUG=False`:

```bash
# Set in .env file
APP_DEBUG=False

# Start the application
uvicorn app.main:app
```

#### Manual

```bash
# Upgrade to latest version
make migrate
# or
alembic upgrade head

# Upgrade to specific revision
alembic upgrade <revision_id>

# Downgrade one revision
make migrate-downgrade
# or
alembic downgrade -1
```

### Viewing Migration Status

```bash
# Show current revision
make migrate-current
# or
alembic current

# Show migration history
make migrate-history
# or
alembic history --verbose
```

## Development Workflow

### Adding a New Model

1. Create your SQLModel model in the appropriate module:
   ```python
   # app/modules/example/models/example.py
   from sqlmodel import SQLModel, Field
   
   class Example(SQLModel, table=True):
       id: int | None = Field(default=None, primary_key=True)
       name: str
   ```

2. Import the model in `alembic/env.py` (if not already imported):
   ```python
   import app.modules.example.models
   ```

3. Create a migration:
   ```bash
   make migrate-create
   # Enter: "Add Example model"
   ```

4. Review the generated migration in `alembic/versions/`

5. Test the migration:
   ```bash
   # Apply migration
   make migrate
   
   # Test downgrade
   make migrate-downgrade
   
   # Re-apply
   make migrate
   ```

### Modifying an Existing Model

1. Update your SQLModel model
2. Create a migration: `make migrate-create`
3. Review and test the migration
4. Commit both the model changes and migration file

## Production Deployment

### Initial Setup

1. Ensure `APP_DEBUG=False` in production environment
2. Install dependencies: `pip install -r requirements.txt`
3. Migrations will run automatically on first startup

### Updating Production

1. Deploy new code with migration files
2. Restart the application
3. Migrations run automatically on startup
4. Monitor logs for migration success/failure

### Manual Migration (if needed)

```bash
# SSH into production server
cd /path/to/app

# Run migrations manually
alembic upgrade head

# Check current version
alembic current
```

## Best Practices

### DO

✅ **Review auto-generated migrations** - Alembic may not detect all changes correctly  
✅ **Test both upgrade and downgrade** - Ensure migrations are reversible  
✅ **Keep migrations atomic** - One logical change per migration  
✅ **Add descriptive messages** - Use clear migration names  
✅ **Backup before migrating** - Always backup production databases  
✅ **Version control migrations** - Commit migration files to git  
✅ **Test in staging first** - Never test migrations in production first  

### DON'T

❌ **Don't edit applied migrations** - Create a new migration instead  
❌ **Don't delete migration files** - They're part of your schema history  
❌ **Don't skip migrations** - Apply them in order  
❌ **Don't mix manual and automatic changes** - Use migrations for all schema changes  
❌ **Don't commit without testing** - Always test migrations locally first  

## Troubleshooting

### "Target database is not up to date"

This means the database has migrations that aren't in your migration history.

```bash
# Mark current database state as up-to-date
alembic stamp head
```

### Migration Conflicts

If multiple developers create migrations simultaneously:

1. Pull latest changes
2. Resolve migration order in `alembic/versions/`
3. Update `down_revision` in newer migration
4. Test the migration chain

### Reset Migrations (Development Only)

⚠️ **WARNING: This will delete all data!**

```bash
# Delete database
rm db.sqlite3

# Delete migration files (keep __init__.py)
rm alembic/versions/*.py

# Create fresh initial migration
alembic revision --autogenerate -m "Initial migration"

# Apply migration
alembic upgrade head
```

### Debugging Migrations

Enable verbose logging in `alembic.ini`:

```ini
[logger_alembic]
level = DEBUG
```

Or run with verbose flag:

```bash
alembic -v upgrade head
```

## Common Scenarios

### Adding a Column with Default Value

```python
# Migration will look like:
def upgrade():
    op.add_column('users', sa.Column('email', sa.String(), nullable=True))
    
    # Set default for existing rows
    op.execute("UPDATE users SET email = 'default@example.com' WHERE email IS NULL")
    
    # Make column non-nullable
    op.alter_column('users', 'email', nullable=False)

def downgrade():
    op.drop_column('users', 'email')
```

### Renaming a Column

```python
def upgrade():
    op.alter_column('users', 'old_name', new_column_name='new_name')

def downgrade():
    op.alter_column('users', 'new_name', new_column_name='old_name')
```

### Data Migration

```python
from alembic import op
import sqlalchemy as sa

def upgrade():
    # Get connection
    connection = op.get_bind()
    
    # Execute data migration
    connection.execute(
        sa.text("UPDATE users SET status = 'active' WHERE status IS NULL")
    )

def downgrade():
    pass  # Data migrations often can't be reversed
```

## Additional Resources

- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)
- [Alembic Tutorial](https://alembic.sqlalchemy.org/en/latest/tutorial.html)
- [Alembic Cookbook](https://alembic.sqlalchemy.org/en/latest/cookbook.html)

## Support

For issues or questions:
1. Check this documentation
2. Review `alembic/README.md`
3. Check Alembic logs in application output
4. Consult the team lead or DevOps