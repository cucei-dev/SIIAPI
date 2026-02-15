"""
Unit tests for core config module
"""
import pytest
import os
from unittest.mock import patch

from app.core.config import get_bool, get_float, Settings


@pytest.mark.unit
class TestGetBool:
    """Test get_bool utility function"""

    def test_get_bool_true_string(self):
        """Test get_bool with 'true' string"""
        assert get_bool("true") is True
        assert get_bool("True") is True
        assert get_bool("TRUE") is True

    def test_get_bool_one_string(self):
        """Test get_bool with '1' string"""
        assert get_bool("1") is True

    def test_get_bool_yes_string(self):
        """Test get_bool with 'yes' string"""
        assert get_bool("yes") is True
        assert get_bool("Yes") is True
        assert get_bool("YES") is True

    def test_get_bool_false_string(self):
        """Test get_bool with false values"""
        assert get_bool("false") is False
        assert get_bool("0") is False
        assert get_bool("no") is False
        assert get_bool("") is False

    def test_get_bool_none_default_false(self):
        """Test get_bool with None and default False"""
        assert get_bool(None) is False

    def test_get_bool_none_default_true(self):
        """Test get_bool with None and default True"""
        assert get_bool(None, default=True) is True


@pytest.mark.unit
class TestGetFloat:
    """Test get_float utility function"""

    def test_get_float_valid_string(self):
        """Test get_float with valid float string"""
        assert get_float("3.14") == 3.14
        assert get_float("0.5") == 0.5
        assert get_float("100.0") == 100.0

    def test_get_float_valid_int_string(self):
        """Test get_float with valid integer string"""
        assert get_float("42") == 42.0
        assert get_float("0") == 0.0

    def test_get_float_invalid_string(self):
        """Test get_float with invalid string"""
        assert get_float("invalid") == 0.0
        assert get_float("abc") == 0.0

    def test_get_float_none_default(self):
        """Test get_float with None"""
        assert get_float(None) == 0.0
        assert get_float(None, default=5.5) == 5.5

    def test_get_float_empty_string(self):
        """Test get_float with empty string"""
        assert get_float("") == 0.0

    def test_get_float_custom_default(self):
        """Test get_float with custom default"""
        assert get_float("invalid", default=10.5) == 10.5


@pytest.mark.unit
class TestSettings:
    """Test Settings class"""

    def test_settings_default_values(self):
        """Test settings with default values"""
        with patch.dict(os.environ, {}, clear=True):
            settings = Settings()
            
            assert settings.DB_URL == "sqlite:///./db.sqlite3"
            assert settings.APP_SITE == "localhost"
            assert settings.APP_ENV == "dev"
            assert settings.APP_VERSION == "0.0.1"
            assert settings.APP_DEBUG is True
            assert settings.SECRET_KEY == "your-secret-key"
            assert settings.ALGORITHM == "HS256"

    def test_settings_from_environment(self):
        """Test settings loaded from environment variables"""
        env_vars = {
            "DB_URL": "postgresql://user:pass@localhost/testdb",
            "APP_NAME": "Test API",
            "APP_SITE": "testsite.com",
            "APP_ENV": "production",
            "APP_DESCRIPTION": "Test Description",
            "APP_DEBUG": "false",
            "SECRET_KEY": "test-secret-key",
            "DUMMY_HASH": "test-dummy-hash",
            "SIIAU_URL": "https://siiau.test.com",
        }
        
        with patch.dict(os.environ, env_vars, clear=True):
            settings = Settings()
            
            assert settings.DB_URL == "postgresql://user:pass@localhost/testdb"
            assert settings.APP_NAME == "Test API"
            assert settings.APP_SITE == "testsite.com"
            assert settings.APP_ENV == "production"
            assert settings.APP_DESCRIPTION == "Test Description"
            assert settings.APP_DEBUG is False
            assert settings.SECRET_KEY == "test-secret-key"
            assert settings.DUMMY_HASH == "test-dummy-hash"
            assert settings.SIIAU_URL == "https://siiau.test.com"

    def test_settings_app_debug_variations(self):
        """Test APP_DEBUG with different values"""
        test_cases = [
            ("true", True),
            ("1", True),
            ("yes", True),
            ("false", False),
            ("0", False),
            ("no", False),
        ]
        
        for value, expected in test_cases:
            with patch.dict(os.environ, {"APP_DEBUG": value}, clear=True):
                settings = Settings()
                assert settings.APP_DEBUG is expected

    def test_settings_algorithm_constant(self):
        """Test that ALGORITHM is always HS256"""
        with patch.dict(os.environ, {}, clear=True):
            settings = Settings()
            assert settings.ALGORITHM == "HS256"

    def test_settings_app_version_constant(self):
        """Test that APP_VERSION is constant"""
        with patch.dict(os.environ, {}, clear=True):
            settings = Settings()
            assert settings.APP_VERSION == "0.0.1"