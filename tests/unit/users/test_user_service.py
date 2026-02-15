"""
Unit tests for user service
"""
import pytest
from unittest.mock import Mock, MagicMock
from sqlmodel import Session

from app.modules.users.services.user_service import UserService
from app.modules.users.repositories.user_repository import UserRepository
from app.modules.users.schemas import UserCreate, UserUpdate
from app.modules.users.models import User
from app.core.exceptions import NotFoundException, ConflictException
from app.core.security import hash_password, verify_password


@pytest.mark.unit
class TestUserServiceCreate:
    """Test UserService create operations"""

    def test_create_user_success(self, session: Session):
        """Test successful user creation"""
        repository = UserRepository(session)
        service = UserService(repository)
        
        user_data = UserCreate(
            name="New User",
            email="newuser@example.com",
            password="password123",
            is_active=True,
        )
        
        created_user = service.create_user(user_data)
        
        assert created_user.id is not None
        assert created_user.name == "New User"
        assert created_user.email == "newuser@example.com"
        assert created_user.is_active is True
        assert verify_password("password123", created_user.password)

    def test_create_user_duplicate_email(self, session: Session, test_user: User):
        """Test creating user with duplicate email"""
        repository = UserRepository(session)
        service = UserService(repository)
        
        user_data = UserCreate(
            name="Duplicate User",
            email=test_user.email,
            password="password123",
            is_active=True,
        )
        
        with pytest.raises(ConflictException) as exc_info:
            service.create_user(user_data)
        
        assert "Email already registered" in str(exc_info.value)

    def test_create_user_with_email_validation(self, session: Session):
        """Test creating user with email validation enabled"""
        repository = UserRepository(session)
        service = UserService(repository)
        
        user_data = UserCreate(
            name="Email Validate User",
            email="emailvalidate@example.com",
            password="password123",
            is_active=True,
        )
        
        created_user = service.create_user(user_data, email_validate=True)
        
        assert created_user.is_active is False

    def test_create_user_password_hashed(self, session: Session):
        """Test that password is hashed on creation"""
        repository = UserRepository(session)
        service = UserService(repository)
        
        plain_password = "plainpassword123"
        user_data = UserCreate(
            name="Hash Test User",
            email="hashtest@example.com",
            password=plain_password,
            is_active=True,
        )
        
        created_user = service.create_user(user_data)
        
        assert created_user.password != plain_password
        assert verify_password(plain_password, created_user.password)


@pytest.mark.unit
class TestUserServiceRead:
    """Test UserService read operations"""

    def test_get_user_success(self, session: Session, test_user: User):
        """Test getting a user by ID"""
        repository = UserRepository(session)
        service = UserService(repository)
        
        user = service.get_user(test_user.id)
        
        assert user.id == test_user.id
        assert user.email == test_user.email

    def test_get_user_not_found(self, session: Session):
        """Test getting a non-existent user"""
        repository = UserRepository(session)
        service = UserService(repository)
        
        with pytest.raises(NotFoundException) as exc_info:
            service.get_user(99999)
        
        assert "User not found" in str(exc_info.value)

    def test_list_users(self, session: Session, test_user: User):
        """Test listing users"""
        repository = UserRepository(session)
        service = UserService(repository)
        
        users, total = service.list_users()
        
        assert total >= 1
        assert len(users) >= 1

    def test_list_users_with_filters(self, session: Session, test_user: User):
        """Test listing users with filters"""
        repository = UserRepository(session)
        service = UserService(repository)
        
        users, total = service.list_users(email=test_user.email)
        
        assert total == 1
        assert users[0].email == test_user.email


@pytest.mark.unit
class TestUserServiceUpdate:
    """Test UserService update operations"""

    def test_update_user_success(self, session: Session, test_user: User):
        """Test successful user update"""
        repository = UserRepository(session)
        service = UserService(repository)
        
        update_data = UserUpdate(
            name="Updated Name",
        )
        
        updated_user = service.update_user(test_user.id, update_data)
        
        assert updated_user.name == "Updated Name"
        assert updated_user.email == test_user.email

    def test_update_user_not_found(self, session: Session):
        """Test updating a non-existent user"""
        repository = UserRepository(session)
        service = UserService(repository)
        
        update_data = UserUpdate(name="New Name")
        
        with pytest.raises(NotFoundException) as exc_info:
            service.update_user(99999, update_data)
        
        assert "User not found" in str(exc_info.value)

    def test_update_user_email(self, session: Session, test_user: User):
        """Test updating user email"""
        repository = UserRepository(session)
        service = UserService(repository)
        
        update_data = UserUpdate(
            email="newemail@example.com",
        )
        
        updated_user = service.update_user(test_user.id, update_data)
        
        assert updated_user.email == "newemail@example.com"

    def test_update_user_duplicate_email(self, session: Session, test_user: User, test_superuser: User):
        """Test updating user with duplicate email"""
        repository = UserRepository(session)
        service = UserService(repository)
        
        update_data = UserUpdate(
            email=test_superuser.email,
        )
        
        with pytest.raises(ConflictException) as exc_info:
            service.update_user(test_user.id, update_data)
        
        assert "Email already registered" in str(exc_info.value)

    def test_update_user_password(self, session: Session, test_user: User):
        """Test updating user password"""
        repository = UserRepository(session)
        service = UserService(repository)
        
        new_password = "newpassword123"
        update_data = UserUpdate(
            password=new_password,
        )
        
        updated_user = service.update_user(test_user.id, update_data)
        
        assert verify_password(new_password, updated_user.password)

    def test_update_user_partial(self, session: Session, test_user: User):
        """Test partial user update"""
        repository = UserRepository(session)
        service = UserService(repository)
        
        original_email = test_user.email
        update_data = UserUpdate(
            name="Partially Updated",
        )
        
        updated_user = service.update_user(test_user.id, update_data)
        
        assert updated_user.name == "Partially Updated"
        assert updated_user.email == original_email


@pytest.mark.unit
class TestUserServiceDelete:
    """Test UserService delete operations"""

    def test_delete_user_soft(self, session: Session, test_user: User):
        """Test soft deleting a user"""
        repository = UserRepository(session)
        service = UserService(repository)
        
        service.delete_user(test_user.id)
        
        user = repository.get(test_user.id)
        assert user.is_active is False

    def test_delete_user_not_found(self, session: Session):
        """Test deleting a non-existent user"""
        repository = UserRepository(session)
        service = UserService(repository)
        
        with pytest.raises(NotFoundException) as exc_info:
            service.delete_user(99999)
        
        assert "User not found" in str(exc_info.value)

    def test_hard_delete_user(self, session: Session):
        """Test hard deleting a user"""
        repository = UserRepository(session)
        service = UserService(repository)
        
        # Create a user to delete
        user_data = UserCreate(
            name="To Delete",
            email="todelete@example.com",
            password="password123",
            is_active=True,
        )
        created_user = service.create_user(user_data)
        
        service.hard_delete_user(created_user.id)
        
        user = repository.get(created_user.id)
        assert user is None

    def test_hard_delete_user_not_found(self, session: Session):
        """Test hard deleting a non-existent user"""
        repository = UserRepository(session)
        service = UserService(repository)
        
        with pytest.raises(NotFoundException) as exc_info:
            service.hard_delete_user(99999)
        
        assert "User not found" in str(exc_info.value)