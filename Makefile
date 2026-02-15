.PHONY: help install test test-unit test-integration test-cov clean lint format

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
	python -c "from app.core.database import init_db; init_db()"

db-seed:
	python -c "from app.core.seed import seed_data; seed_data()"