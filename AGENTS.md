# AGENTS.md — Essential Guidance for SIIAPI

This repo is a modular FastAPI + SQLModel REST API for university academic data (SIIAU integration, multi-module, JWT auth). This file is for OpenCode and similar coding agents. **Keep this file ruthlessly compact and surgery-focused.**

---

## High-Signal Conventions

- **Never guess commands**. Use `make` targets or `dev.sh` when available—these are source of truth for all build, test, lint, and DB flows.
- **Dev database is wiped** by `dev.sh` (removes `db.sqlite3` before launch). Do not use in production.
- **Config always via `.env`**; see `.env.example` for required names. Do not hardcode secrets. All settings are loaded by `app/core/config.py` at startup.
    - `APP_DEBUG=true` — Uses `SQLModel.metadata.create_all()`, runs seed data on start, ignores Alembic.
    - `APP_DEBUG=false` — Uses Alembic on app start, seed only via `make db-seed` or the manual script.
- **Seeding**: Only run `make db-seed` or `python scripts/seed_database.py`; does not run automatically in production. Seeds just the admin user (see `app/core/seed.py`).
- **Database migrations**: Run only via `make migrate`, `make migrate-create`, etc. in production. See `alembic/README.md` for edge cases/recovery commands.
- **Makefile targets always reflect reality.** If they drift, update Makefile and this file.

---

## Key Commands (copy/paste-ready)

- `make install` — Install all test/dev dependencies (uses `requirements-test.txt`).
- `make dev` — Launch dev server (`uvicorn ... --reload`).
- `./dev.sh` — Wipes DB, launches in development mode (for new schemas, resets, demos only).
- `make test / make test-unit / make test-integration / make test-cov` — Full, unit, integration, coverage.
- `pytest ...` — Use direct pytest for class/function targeting (see `pytest.ini` for custom markers).
- **Single test:** `pytest path/to/file.py::ClassName::test_func`
- **Lint/format:** `make lint`, `make format`. Always check before PR.
- **Database:**
    - `make db-init` — Dev DB init via SQLModel.
    - `make migrate` — Alembic to head (prod only).
    - `make migrate-create` — Create migration after model changes (interactive message, see Makefile).
    - `make db-seed` — Run seed script (admin user only by default).

---

## Testing Workflow Quirks
- Test structure and expectations are defined in `tests/README.md`. Use markers (unit, integration, auth, database, slow) as shown in `pytest.ini` and README.
- All test coverage options, fixtures, and strategies are documented in `tests/README.md`—do not duplicate here.
- Pytest config (`pytest.ini`): strict markers are enforced.

---

## Structure/Architecture
- **Modules:** Each feature is under `app/modules/{feature}/` with subfolders for `api/`, `models/`, `repositories/`, `schemas/`, `services/`.
- **Entrypoints:**
    - App: `app/main.py`
    - API routes: `app/api/routes.py`
    - DB/init: `app/core/database.py`, migrations in `alembic/`
    - Seed data: `app/core/seed.py` (called only from manual script)
- **Production**: Strict .env required, DB migrations critical (do not use dev.sh or DB auto-create). Back up before migrations as per `alembic/README.md`.

---

## Update Process
- Update this file *immediately* if Makefile, environment, seeding, or testing patterns change. Err on the side of deletion for any advice that becomes obvious or is codified elsewhere.

---

_If you are not sure whether a line belongs here, it probably doesn’t._
