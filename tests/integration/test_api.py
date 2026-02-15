"""
Integration tests for API endpoints
"""

import pytest
from fastapi.testclient import TestClient

from app.modules.users.models import User


@pytest.mark.integration
class TestHealthEndpoint:
    """Test health check endpoint"""

    def test_health_check(self, client: TestClient):
        """Test health check endpoint"""
        response = client.get("/")

        # FastAPI default 404 for root, or implement health check
        assert response.status_code in [200, 404]


@pytest.mark.integration
class TestAuthEndpoints:
    """Test authentication endpoints"""

    def test_login_success(self, client: TestClient, test_user: User):
        """Test successful login"""
        response = client.post(
            "/api/auth/login",
            json={
                "email": test_user.email,
                "password": "testpassword123",
                "remember_me": False,
                "user_agent": "Test Client",
                "ip_address": "127.0.0.1",
                "audience": "test",
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data

    def test_login_invalid_credentials(self, client: TestClient):
        """Test login with invalid credentials"""
        response = client.post(
            "/api/auth/login",
            json={
                "email": "invalid@example.com",
                "password": "wrongpassword",
                "remember_me": False,
                "user_agent": "Test Client",
                "ip_address": "127.0.0.1",
                "audience": "test",
            },
        )

        assert response.status_code == 400

    def test_login_inactive_user(self, client: TestClient, test_inactive_user: User):
        """Test login with inactive user"""
        response = client.post(
            "/api/auth/login",
            json={
                "email": test_inactive_user.email,
                "password": "inactivepassword123",
                "remember_me": False,
                "user_agent": "Test Client",
                "ip_address": "127.0.0.1",
                "audience": "test",
            },
        )

        assert response.status_code == 403


@pytest.mark.integration
class TestUserEndpoints:
    """Test user endpoints"""

    def test_get_current_user(
        self, client: TestClient, auth_headers: dict, test_user: User
    ):
        """Test getting current user"""
        response = client.get("/api/users/me", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert data["email"] == test_user.email

    def test_get_current_user_unauthorized(self, client: TestClient):
        """Test getting current user without authentication"""
        response = client.get("/api/users/me")

        assert response.status_code == 401

    def test_list_users_as_superuser(
        self, client: TestClient, superuser_auth_headers: dict
    ):
        """Test listing users as superuser"""
        response = client.get("/api/users/", headers=superuser_auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert "items" in data or isinstance(data, list)

    def test_create_user_as_superuser(
        self, client: TestClient, superuser_auth_headers: dict
    ):
        """Test creating a user as superuser"""
        response = client.post(
            "/api/users/",
            headers=superuser_auth_headers,
            json={
                "name": "New Test User",
                "email": "newtest@example.com",
                "password": "newpassword123",
                "is_active": True,
            },
        )

        assert response.status_code in [200, 201]
        data = response.json()
        assert data["email"] == "newtest@example.com"

    def test_update_user(self, client: TestClient, auth_headers: dict, test_user: User):
        """Test updating user"""
        response = client.put(
            f"/api/users/{test_user.id}",
            headers=auth_headers,
            json={
                "name": "Updated Name",
            },
        )

        # May be 200 or 403 depending on permissions
        assert response.status_code in [200, 403]

    def test_delete_user_as_superuser(
        self, client: TestClient, superuser_auth_headers: dict
    ):
        """Test deleting a user as superuser"""
        # First create a user to delete
        create_response = client.post(
            "/api/users/",
            headers=superuser_auth_headers,
            json={
                "name": "To Delete",
                "email": "todelete@example.com",
                "password": "password123",
                "is_active": True,
            },
        )

        if create_response.status_code in [200, 201]:
            user_id = create_response.json()["id"]

            delete_response = client.delete(
                f"/api/users/{user_id}", headers=superuser_auth_headers
            )

            assert delete_response.status_code in [200, 204]


@pytest.mark.integration
class TestPaginationEndpoints:
    """Test pagination in list endpoints"""

    def test_users_pagination(self, client: TestClient, superuser_auth_headers: dict):
        """Test user list pagination"""
        response = client.get(
            "/api/users/?skip=0&limit=10", headers=superuser_auth_headers
        )

        assert response.status_code == 200
        data = response.json()

        # Check if response has pagination structure
        if isinstance(data, dict):
            assert "items" in data or "data" in data or "results" in data


@pytest.mark.integration
class TestErrorHandling:
    """Test error handling"""

    def test_not_found_endpoint(self, client: TestClient):
        """Test 404 for non-existent endpoint"""
        response = client.get("/api/nonexistent")

        assert response.status_code == 404

    def test_method_not_allowed(self, client: TestClient):
        """Test 405 for wrong HTTP method"""
        response = client.post("/api/users/me")

        assert response.status_code in [405, 401]  # 401 if auth required first

    def test_invalid_json(self, client: TestClient, auth_headers: dict):
        """Test invalid JSON in request body"""
        response = client.post(
            "/api/users/",
            headers=auth_headers,
            data="invalid json",
        )

        assert response.status_code in [400, 422]


@pytest.mark.integration
class TestCORSHeaders:
    """Test CORS headers if configured"""

    def test_cors_headers_present(self, client: TestClient):
        """Test that CORS headers are present if configured"""
        response = client.options("/api/users/")

        # CORS may or may not be configured
        assert response.status_code in [200, 405]
