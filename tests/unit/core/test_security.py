"""
Unit tests for core security module
"""
import pytest
from datetime import datetime, timedelta
from jose import jwt

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    check_token,
    encrypt,
    decrypt,
)
from app.core.config import settings
from app.modules.auth.schemas import AccessTokenData, RefreshTokenData


@pytest.mark.unit
class TestPasswordHashing:
    """Test password hashing and verification"""

    def test_hash_password(self):
        """Test password hashing"""
        password = "testpassword123"
        hashed = hash_password(password)
        
        assert hashed != password
        assert len(hashed) > 0
        assert hashed.startswith("$2b$")

    def test_verify_password_correct(self):
        """Test password verification with correct password"""
        password = "testpassword123"
        hashed = hash_password(password)
        
        assert verify_password(password, hashed) is True

    def test_verify_password_incorrect(self):
        """Test password verification with incorrect password"""
        password = "testpassword123"
        wrong_password = "wrongpassword"
        hashed = hash_password(password)
        
        assert verify_password(wrong_password, hashed) is False

    def test_verify_password_with_dummy_hash(self):
        """Test password verification with dummy hash (timing attack prevention)"""
        password = "testpassword123"
        
        # Should not raise exception even with dummy hash
        result = verify_password(password)
        assert isinstance(result, bool)


@pytest.mark.unit
class TestAccessToken:
    """Test access token creation and validation"""

    def test_create_access_token(self):
        """Test access token creation"""
        data = AccessTokenData(
            sub="test@example.com",
            is_superuser=False,
            is_staff=False,
            aud="test",
        )
        
        token = create_access_token(data)
        
        assert token.token is not None
        assert token.data.sub == "test@example.com"
        assert token.data.is_superuser is False
        assert token.data.is_staff is False
        assert token.data.aud == "test"
        assert token.data.exp is not None
        assert token.data.iat is not None
        assert token.data.iss == settings.APP_SITE
        assert token.data.jti is not None
        assert token.hash is not None

    def test_access_token_expiration(self):
        """Test access token expiration time"""
        data = AccessTokenData(
            sub="test@example.com",
            is_superuser=False,
            is_staff=False,
            aud="test",
        )
        
        token = create_access_token(data)
        
        # Token should expire in approximately 1 day
        exp_time = datetime.fromtimestamp(token.data.exp)
        iat_time = datetime.fromtimestamp(token.data.iat)
        time_diff = exp_time - iat_time
        
        assert time_diff.days == 1

    def test_access_token_decode(self):
        """Test decoding access token"""
        data = AccessTokenData(
            sub="test@example.com",
            is_superuser=True,
            is_staff=True,
            aud="test",
        )
        
        token = create_access_token(data)
        
        # Decode token
        decoded = jwt.decode(
            token.token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        
        assert decoded["sub"] == "test@example.com"
        assert decoded["is_superuser"] is True
        assert decoded["is_staff"] is True


@pytest.mark.unit
class TestRefreshToken:
    """Test refresh token creation and validation"""

    def test_create_refresh_token(self):
        """Test refresh token creation"""
        data = RefreshTokenData(
            sub="test@example.com",
        )
        
        token = create_refresh_token(data)
        
        assert token.token is not None
        assert token.data.sub == "test@example.com"
        assert token.data.exp is not None
        assert token.data.iat is not None
        assert token.data.jti is not None
        assert token.token_hash is not None

    def test_refresh_token_expiration(self):
        """Test refresh token expiration time"""
        data = RefreshTokenData(
            sub="test@example.com",
        )
        
        token = create_refresh_token(data)
        
        # Token should expire in approximately 1 day
        exp_time = datetime.fromtimestamp(token.data.exp)
        iat_time = datetime.fromtimestamp(token.data.iat)
        time_diff = exp_time - iat_time
        
        assert time_diff.days == 1


@pytest.mark.unit
class TestCheckToken:
    """Test token validation"""

    def test_check_token_valid_access(self):
        """Test checking valid access token"""
        data = AccessTokenData(
            sub="test@example.com",
            is_superuser=False,
            is_staff=False,
            aud=settings.APP_ENV,
            type="access",
        )
        
        token = create_access_token(data)
        result = check_token(token.token, "access")
        
        assert result is not None
        assert result["sub"] == "test@example.com"
        assert result["type"] == "access"

    def test_check_token_valid_refresh(self):
        """Test checking valid refresh token"""
        data = RefreshTokenData(
            sub="test@example.com",
            type="refresh",
            aud=settings.APP_ENV,
        )
        
        token = create_refresh_token(data)
        result = check_token(token.token, "refresh")
        
        assert result is not None
        assert result["sub"] == "test@example.com"
        assert result["type"] == "refresh"

    def test_check_token_wrong_type(self):
        """Test checking token with wrong type"""
        data = AccessTokenData(
            sub="test@example.com",
            is_superuser=False,
            is_staff=False,
            aud=settings.APP_ENV,
            type="access",
        )
        
        token = create_access_token(data)
        result = check_token(token.token, "refresh")
        
        assert result is None

    def test_check_token_invalid(self):
        """Test checking invalid token"""
        result = check_token("invalid_token", "access")
        
        assert result is None

    def test_check_token_expired(self):
        """Test checking expired token"""
        # Create token with past expiration
        now = datetime.now()
        past = now - timedelta(days=2)
        
        payload = {
            "sub": "test@example.com",
            "type": "access",
            "aud": settings.APP_ENV,
            "exp": int(past.timestamp()),
            "iat": int((past - timedelta(days=1)).timestamp()),
        }
        
        expired_token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        result = check_token(expired_token, "access")
        
        assert result is None


@pytest.mark.unit
class TestEncryption:
    """Test encryption and decryption"""

    def test_encrypt_decrypt(self):
        """Test encrypting and decrypting a message"""
        message = "This is a secret message"
        
        encrypted = encrypt(message)
        assert encrypted != message
        assert "$" in encrypted
        
        decrypted = decrypt(encrypted)
        assert decrypted == message

    def test_encrypt_empty_string(self):
        """Test encrypting empty string"""
        message = ""
        
        encrypted = encrypt(message)
        decrypted = decrypt(encrypted)
        
        assert decrypted == message

    def test_encrypt_special_characters(self):
        """Test encrypting message with special characters"""
        message = "Test!@#$%^&*()_+-=[]{}|;:',.<>?/~`"
        
        encrypted = encrypt(message)
        decrypted = decrypt(encrypted)
        
        assert decrypted == message

    def test_encrypt_unicode(self):
        """Test encrypting unicode characters"""
        message = "Hello 世界 🌍"
        
        encrypted = encrypt(message)
        decrypted = decrypt(encrypted)
        
        assert decrypted == message

    def test_decrypt_with_custom_split(self):
        """Test decrypting with custom split character"""
        message = "Test message"
        
        encrypted = encrypt(message)
        # Replace $ with custom separator
        custom_encrypted = encrypted.replace("$", "|")
        
        decrypted = decrypt(custom_encrypted, split="|")
        assert decrypted == message