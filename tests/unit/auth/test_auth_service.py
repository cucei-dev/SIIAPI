"""
Unit tests for auth service
"""

from datetime import datetime, timedelta
from unittest.mock import Mock, patch

import pytest
from sqlmodel import Session

from app.core.exceptions import (BadRequestException, ForbiddenException,
                                 UnauthorizedException)
from app.core.security import hash_password
from app.modules.auth.schemas import LoginData, RefreshTokenRequest
from app.modules.auth.services.auth_service import AuthService
from app.modules.auth.services.refresh_token_service import RefreshTokenService
from app.modules.users.models import User
from app.modules.users.repositories.user_repository import UserRepository


@pytest.mark.unit
class TestAuthServiceLogin:
    """Test AuthService login operations"""

    def test_login_success(self, session: Session, test_user: User):
        """Test successful login"""
        user_repository = UserRepository(session)
        refresh_token_service = RefreshTokenService(Mock())
        service = AuthService(refresh_token_service, user_repository)

        login_data = LoginData(
            email=test_user.email,
            password="testpassword123",
            remember_me=False,
            user_agent="Test Agent",
            ip_address="127.0.0.1",
            audience="test",
        )

        with patch.object(refresh_token_service, "create_refresh_token"):
            response = service.login(login_data)

        assert response.access_token is not None
        assert response.refresh_token is not None
        assert response.access_token_expires_at is not None
        assert response.refresh_token_expires_at is not None

    def test_login_invalid_email(self, session: Session):
        """Test login with invalid email"""
        user_repository = UserRepository(session)
        refresh_token_service = RefreshTokenService(Mock())
        service = AuthService(refresh_token_service, user_repository)

        login_data = LoginData(
            email="nonexistent@example.com",
            password="password123",
            remember_me=False,
            user_agent="Test Agent",
            ip_address="127.0.0.1",
            audience="test",
        )

        with pytest.raises(BadRequestException) as exc_info:
            service.login(login_data)

        assert "Invalid email or password" in str(exc_info.value)

    def test_login_invalid_password(self, session: Session, test_user: User):
        """Test login with invalid password"""
        user_repository = UserRepository(session)
        refresh_token_service = RefreshTokenService(Mock())
        service = AuthService(refresh_token_service, user_repository)

        login_data = LoginData(
            email=test_user.email,
            password="wrongpassword",
            remember_me=False,
            user_agent="Test Agent",
            ip_address="127.0.0.1",
            audience="test",
        )

        with pytest.raises(BadRequestException) as exc_info:
            service.login(login_data)

        assert "Invalid email or password" in str(exc_info.value)

    def test_login_inactive_user(self, session: Session, test_inactive_user: User):
        """Test login with inactive user"""
        user_repository = UserRepository(session)
        refresh_token_service = RefreshTokenService(Mock())
        service = AuthService(refresh_token_service, user_repository)

        login_data = LoginData(
            email=test_inactive_user.email,
            password="inactivepassword123",
            remember_me=False,
            user_agent="Test Agent",
            ip_address="127.0.0.1",
            audience="test",
        )

        with pytest.raises(ForbiddenException) as exc_info:
            service.login(login_data)

        assert "User is inactive" in str(exc_info.value)

    def test_login_updates_last_login(self, session: Session, test_user: User):
        """Test that login updates last_login timestamp"""
        user_repository = UserRepository(session)
        refresh_token_service = RefreshTokenService(Mock())
        service = AuthService(refresh_token_service, user_repository)

        original_last_login = test_user.last_login

        login_data = LoginData(
            email=test_user.email,
            password="testpassword123",
            remember_me=False,
            user_agent="Test Agent",
            ip_address="127.0.0.1",
            audience="test",
        )

        with patch.object(refresh_token_service, "create_refresh_token"):
            service.login(login_data)

        updated_user = user_repository.get(test_user.id)
        assert updated_user.last_login != original_last_login
        assert updated_user.last_login is not None


@pytest.mark.unit
class TestAuthServiceCreateTokens:
    """Test AuthService token creation"""

    def test_create_tokens_with_refresh(self, session: Session, test_user: User):
        """Test creating tokens with refresh token"""
        user_repository = UserRepository(session)
        refresh_token_service = RefreshTokenService(Mock())
        service = AuthService(refresh_token_service, user_repository)

        login_data = LoginData(
            email=test_user.email,
            password="testpassword123",
            remember_me=False,
            user_agent="Test Agent",
            ip_address="127.0.0.1",
            audience="test",
        )

        with patch.object(refresh_token_service, "create_refresh_token"):
            response = service.create_tokens(
                login_data=login_data,
                user=test_user,
                temporary=False,
                refresh=True,
            )

        assert response.access_token is not None
        assert response.refresh_token is not None

    def test_create_tokens_temporary(self, session: Session, test_user: User):
        """Test creating temporary tokens (no refresh token)"""
        user_repository = UserRepository(session)
        refresh_token_service = RefreshTokenService(Mock())
        service = AuthService(refresh_token_service, user_repository)

        login_data = LoginData(
            email=test_user.email,
            password="testpassword123",
            remember_me=False,
            user_agent="Test Agent",
            ip_address="127.0.0.1",
            audience="test",
        )

        response = service.create_tokens(
            login_data=login_data,
            user=test_user,
            temporary=True,
            refresh=False,
        )

        assert response.access_token is not None
        assert response.refresh_token is None
        assert response.refresh_token_expires_at is None


@pytest.mark.unit
class TestAuthServiceLogout:
    """Test AuthService logout operations"""

    def test_logout_success(self, session: Session, test_user: User):
        """Test successful logout"""
        user_repository = UserRepository(session)

        # Create mock refresh token service
        mock_refresh_token = Mock()
        mock_refresh_token.is_active = True
        mock_refresh_token.user_agent = "Test Agent"
        mock_refresh_token.ip_address = "127.0.0.1"
        mock_refresh_token.expires_at = datetime.now() + timedelta(days=1)
        mock_refresh_token.created_at = datetime.now() - timedelta(hours=1)
        mock_refresh_token.user = test_user
        mock_refresh_token.user_id = test_user.id
        mock_refresh_token.jti = "test-jti"
        mock_refresh_token.token_hash = hash_password("test-token")

        refresh_token_service = Mock()
        refresh_token_service.get_refresh_token.return_value = mock_refresh_token

        service = AuthService(refresh_token_service, user_repository)

        logout_data = RefreshTokenRequest(
            refresh_token="test-token",
            user_agent="Test Agent",
            ip_address="127.0.0.1",
        )

        with patch("app.modules.auth.services.auth_service.check_token") as mock_check:
            mock_check.return_value = {"jti": "test-jti"}
            with patch(
                "app.modules.auth.services.auth_service.verify_password"
            ) as mock_verify:
                mock_verify.return_value = True
                result = service.logout(logout_data, test_user)

        assert result is None
        refresh_token_service.delete_refresh_token.assert_called_once_with("test-jti")

    def test_logout_invalid_token(self, session: Session, test_user: User):
        """Test logout with invalid token"""
        user_repository = UserRepository(session)
        refresh_token_service = Mock()
        service = AuthService(refresh_token_service, user_repository)

        logout_data = RefreshTokenRequest(
            refresh_token="invalid-token",
            user_agent="Test Agent",
            ip_address="127.0.0.1",
        )

        with patch("app.modules.auth.services.auth_service.check_token") as mock_check:
            mock_check.return_value = None

            with pytest.raises(UnauthorizedException) as exc_info:
                service.logout(logout_data, test_user)

            assert "Invalid refresh token" in str(exc_info.value)

    def test_logout_inactive_token(self, session: Session, test_user: User):
        """Test logout with inactive token"""
        user_repository = UserRepository(session)

        mock_refresh_token = Mock()
        mock_refresh_token.is_active = False

        refresh_token_service = Mock()
        refresh_token_service.get_refresh_token.return_value = mock_refresh_token

        service = AuthService(refresh_token_service, user_repository)

        logout_data = RefreshTokenRequest(
            refresh_token="test-token",
            user_agent="Test Agent",
            ip_address="127.0.0.1",
        )

        with patch("app.modules.auth.services.auth_service.check_token") as mock_check:
            mock_check.return_value = {"jti": "test-jti"}

            with pytest.raises(UnauthorizedException) as exc_info:
                service.logout(logout_data, test_user)

            assert "Refresh token is inactive" in str(exc_info.value)

    def test_logout_expired_token(self, session: Session, test_user: User):
        """Test logout with expired token"""
        user_repository = UserRepository(session)

        mock_refresh_token = Mock()
        mock_refresh_token.is_active = True
        mock_refresh_token.user_agent = "Test Agent"
        mock_refresh_token.ip_address = "127.0.0.1"
        mock_refresh_token.expires_at = datetime.now() - timedelta(days=1)

        refresh_token_service = Mock()
        refresh_token_service.get_refresh_token.return_value = mock_refresh_token

        service = AuthService(refresh_token_service, user_repository)

        logout_data = RefreshTokenRequest(
            refresh_token="test-token",
            user_agent="Test Agent",
            ip_address="127.0.0.1",
        )

        with patch("app.modules.auth.services.auth_service.check_token") as mock_check:
            mock_check.return_value = {"jti": "test-jti"}

            with pytest.raises(UnauthorizedException) as exc_info:
                service.logout(logout_data, test_user)

            assert "Refresh token is expired" in str(exc_info.value)

    def test_logout_mismatched_user_agent(self, session: Session, test_user: User):
        """Test logout with mismatched user agent"""
        user_repository = UserRepository(session)

        mock_refresh_token = Mock()
        mock_refresh_token.is_active = True
        mock_refresh_token.user_agent = "Different Agent"
        mock_refresh_token.ip_address = "127.0.0.1"

        refresh_token_service = Mock()
        refresh_token_service.get_refresh_token.return_value = mock_refresh_token

        service = AuthService(refresh_token_service, user_repository)

        logout_data = RefreshTokenRequest(
            refresh_token="test-token",
            user_agent="Test Agent",
            ip_address="127.0.0.1",
        )

        with patch("app.modules.auth.services.auth_service.check_token") as mock_check:
            mock_check.return_value = {"jti": "test-jti"}

            with pytest.raises(UnauthorizedException) as exc_info:
                service.logout(logout_data, test_user)

            assert "Refresh token is invalid" in str(exc_info.value)
