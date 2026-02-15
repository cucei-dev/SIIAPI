# Test Suite Documentation

This directory contains the comprehensive test suite for the SIIAPI project.

## Structure

```
tests/
├── conftest.py              # Pytest configuration and shared fixtures
├── unit/                    # Unit tests
│   ├── core/               # Core module tests
│   │   ├── test_config.py
│   │   └── test_security.py
│   ├── users/              # User module tests
│   │   ├── test_user_repository.py
│   │   └── test_user_service.py
│   └── auth/               # Auth module tests
│       └── test_auth_service.py
└── integration/            # Integration tests
    └── test_api.py
```

## Running Tests

### Install Test Dependencies

```bash
pip install -r requirements-test.txt
```

### Run All Tests

```bash
pytest
```

### Run Specific Test Categories

```bash
# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration

# Run only database tests
pytest -m database

# Run only auth tests
pytest -m auth
```

### Run Tests with Coverage

```bash
pytest --cov=app --cov-report=html
```

This will generate an HTML coverage report in `htmlcov/index.html`.

### Run Tests in Verbose Mode

```bash
pytest -v
```

### Run Specific Test File

```bash
pytest tests/unit/core/test_security.py
```

### Run Specific Test Class or Function

```bash
# Run specific test class
pytest tests/unit/users/test_user_service.py::TestUserServiceCreate

# Run specific test function
pytest tests/unit/users/test_user_service.py::TestUserServiceCreate::test_create_user_success
```

## Test Fixtures

The test suite uses several fixtures defined in `conftest.py`:

### Database Fixtures

- `test_engine`: In-memory SQLite database engine for testing
- `session`: Database session for each test
- `client`: FastAPI TestClient with database override

### User Fixtures

- `test_user`: Regular active user for testing
- `test_superuser`: Superuser with admin privileges
- `test_inactive_user`: Inactive user for testing access control

### Authentication Fixtures

- `auth_headers`: Authentication headers for regular user
- `superuser_auth_headers`: Authentication headers for superuser

## Writing Tests

### Unit Test Example

```python
import pytest
from app.modules.users.services.user_service import UserService

@pytest.mark.unit
class TestUserService:
    def test_create_user(self, session):
        """Test user creation"""
        service = UserService(session)
        # Test implementation
```

### Integration Test Example

```python
import pytest
from fastapi.testclient import TestClient

@pytest.mark.integration
class TestUserAPI:
    def test_get_users(self, client: TestClient, auth_headers: dict):
        """Test GET /api/users endpoint"""
        response = client.get("/api/users/", headers=auth_headers)
        assert response.status_code == 200
```

## Test Markers

The test suite uses the following pytest markers:

- `@pytest.mark.unit`: Unit tests (isolated, fast)
- `@pytest.mark.integration`: Integration tests (API endpoints)
- `@pytest.mark.slow`: Slow-running tests
- `@pytest.mark.auth`: Authentication-related tests
- `@pytest.mark.database`: Database-related tests

## Coverage Goals

The test suite aims for:

- **Overall Coverage**: > 80%
- **Core Modules**: > 90%
- **Business Logic**: > 85%
- **API Endpoints**: > 75%

## Best Practices

1. **Isolation**: Each test should be independent and not rely on other tests
2. **Clarity**: Test names should clearly describe what is being tested
3. **Arrange-Act-Assert**: Follow the AAA pattern in test structure
4. **Fixtures**: Use fixtures for common setup to avoid code duplication
5. **Mocking**: Mock external dependencies to keep tests fast and reliable
6. **Edge Cases**: Test both happy paths and error conditions

## Continuous Integration

Tests are automatically run on:

- Every commit to feature branches
- Pull requests to main/develop branches
- Before deployment to staging/production

## Troubleshooting

### Database Errors

If you encounter database-related errors:

```bash
# Clear test database
rm -f test.db

# Recreate database schema
pytest --create-db
```

### Import Errors

If you encounter import errors:

```bash
# Ensure you're in the project root
cd /path/to/SIIAPI

# Install in development mode
pip install -e .
```

### Slow Tests

To identify slow tests:

```bash
pytest --durations=10
```

## Contributing

When adding new features:

1. Write tests first (TDD approach recommended)
2. Ensure all tests pass before committing
3. Maintain or improve code coverage
4. Update this documentation if adding new test categories

## Test Data

Test data is generated using:

- Fixtures in `conftest.py`
- Factory patterns for complex objects
- Faker library for realistic test data (when needed)

## Security Testing

Security-related tests include:

- Password hashing and verification
- Token generation and validation
- Authentication and authorization
- Input validation and sanitization
- SQL injection prevention (via SQLModel/SQLAlchemy)

## Performance Testing

For performance testing:

```bash
# Run with profiling
pytest --profile

# Run with timing information
pytest --durations=0
```

## Additional Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [SQLModel Testing](https://sqlmodel.tiangolo.com/tutorial/testing/)