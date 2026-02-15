.PHONY: help install test test-unit test-integration test-cov clean lint format migrate

help:
	@echo "Available commands:"
	@echo "  make install          - Install dependencies"
	@echo "  make test             - Run all tests"
	@echo "  make test-unit        - Run unit tests only"
	@echo "  make test-integration - Run integration tests only"
	@echo "  make test-cov         - Run tests with coverage report"
	@echo "  make lint             - Run linters"
	@echo "  make format           - Format code with black and isort"
	@echo "  make clean            - Clean up generated files"
	@echo ""
	@echo "Database commands:"
	@echo "  make db-init          - Initialize database (development)"
	@echo "  make db-seed          - Seed database with test data"
	@echo "  make migrate          - Run database migrations"
	@echo "  make migrate-create   - Create a new migration (autogenerate)"
	@echo "  make migrate-history  - Show migration history"
	@echo "  make migrate-current  - Show current migration revision"
	@echo "  make migrate-downgrade - Downgrade one migration"

install:
	pip install -r requirements-test.txt

test:
	pytest

test-unit:
	pytest -m unit

test-integration:
	pytest -m integration

test-cov:
	pytest --cov=app --cov-report=html --cov-report=term-missing

test-watch:
	pytest-watch

lint:
	flake8 app tests
	black --check app tests
	isort --check-only app tests

format:
	black app tests
	isort app tests

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.coverage" -delete
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf coverage.xml
	rm -rf *.egg-info
	rm -rf dist/
	rm -rf build/

dev:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

db-init:
	@echo "Initializing database schema (development only)..."
	python -c "from app.core.database import init_db; init_db()"

db-seed:
	@echo "Seeding database with initial data..."
	python scripts/seed_database.py

# Alembic migration commands
migrate:
	alembic upgrade head

migrate-create:
	@read -p "Enter migration message: " msg; \
	alembic revision --autogenerate -m "$$msg"

migrate-history:
	alembic history --verbose

migrate-current:
	alembic current

migrate-downgrade:
	alembic downgrade -1