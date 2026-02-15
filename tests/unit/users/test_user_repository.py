"""
Unit tests for user repository
"""

import pytest
from sqlmodel import Session

from app.core.security import hash_password
from app.modules.users.models import User
from app.modules.users.repositories.user_repository import UserRepository


@pytest.mark.unit
@pytest.mark.database
class TestUserRepository:
    """Test UserRepository class"""

    def test_create_user(self, session: Session):
        """Test creating a user"""
        repository = UserRepository(session)

        user = User(
            name="New User",
            email="newuser@example.com",
            password=hash_password("password123"),
            is_active=True,
        )

        created_user = repository.create(user)

        assert created_user.id is not None
        assert created_user.name == "New User"
        assert created_user.email == "newuser@example.com"
        assert created_user.is_active is True

    def test_get_user_by_id(self, session: Session, test_user: User):
        """Test getting a user by ID"""
        repository = UserRepository(session)

        user = repository.get(test_user.id)

        assert user is not None
        assert user.id == test_user.id
        assert user.email == test_user.email

    def test_get_user_not_found(self, session: Session):
        """Test getting a non-existent user"""
        repository = UserRepository(session)

        user = repository.get(99999)

        assert user is None

    def test_list_users_no_filters(self, session: Session, test_user: User):
        """Test listing users without filters"""
        repository = UserRepository(session)

        users, total = repository.list({})

        assert total >= 1
        assert len(users) >= 1
        assert any(u.id == test_user.id for u in users)

    def test_list_users_filter_by_email(self, session: Session, test_user: User):
        """Test listing users filtered by email"""
        repository = UserRepository(session)

        users, total = repository.list({"email": test_user.email})

        assert total == 1
        assert len(users) == 1
        assert users[0].email == test_user.email

    def test_list_users_filter_by_is_active(
        self, session: Session, test_user: User, test_inactive_user: User
    ):
        """Test listing users filtered by is_active"""
        repository = UserRepository(session)

        active_users, active_total = repository.list({"is_active": True})
        inactive_users, inactive_total = repository.list({"is_active": False})

        assert active_total >= 1
        assert inactive_total >= 1
        assert all(u.is_active for u in active_users)
        assert all(not u.is_active for u in inactive_users)

    def test_list_users_filter_by_is_superuser(
        self, session: Session, test_superuser: User
    ):
        """Test listing users filtered by is_superuser"""
        repository = UserRepository(session)

        superusers, total = repository.list({"is_superuser": True})

        assert total >= 1
        assert all(u.is_superuser for u in superusers)

    def test_list_users_filter_by_is_staff(
        self, session: Session, test_superuser: User
    ):
        """Test listing users filtered by is_staff"""
        repository = UserRepository(session)

        staff_users, total = repository.list({"is_staff": True})

        assert total >= 1
        assert all(u.is_staff for u in staff_users)

    def test_list_users_search_by_name(self, session: Session, test_user: User):
        """Test searching users by name"""
        repository = UserRepository(session)

        users, total = repository.list({"search": "Test"})

        assert total >= 1
        assert any(u.id == test_user.id for u in users)

    def test_list_users_search_by_email(self, session: Session, test_user: User):
        """Test searching users by email"""
        repository = UserRepository(session)

        users, total = repository.list({"search": "test@"})

        assert total >= 1
        assert any(u.id == test_user.id for u in users)

    def test_list_users_pagination(self, session: Session):
        """Test user list pagination"""
        repository = UserRepository(session)

        # Create multiple users
        for i in range(5):
            user = User(
                name=f"User {i}",
                email=f"user{i}@example.com",
                password=hash_password("password"),
                is_active=True,
            )
            repository.create(user)

        # Test pagination
        users_page1, total = repository.list({"skip": 0, "limit": 2})
        users_page2, _ = repository.list({"skip": 2, "limit": 2})

        assert len(users_page1) == 2
        assert len(users_page2) == 2
        assert users_page1[0].id != users_page2[0].id

    def test_update_user(self, session: Session, test_user: User):
        """Test updating a user"""
        repository = UserRepository(session)

        test_user.name = "Updated Name"
        updated_user = repository.update(test_user)

        assert updated_user.name == "Updated Name"
        assert updated_user.updated_at is not None

    def test_delete_user(self, session: Session):
        """Test deleting a user"""
        repository = UserRepository(session)

        user = User(
            name="To Delete",
            email="delete@example.com",
            password=hash_password("password"),
            is_active=True,
        )
        created_user = repository.create(user)

        repository.delete(created_user)

        deleted_user = repository.get(created_user.id)
        assert deleted_user is None

    def test_list_users_multiple_filters(self, session: Session, test_user: User):
        """Test listing users with multiple filters"""
        repository = UserRepository(session)

        users, total = repository.list(
            {
                "is_active": True,
                "is_superuser": False,
            }
        )

        assert all(u.is_active for u in users)
        assert all(not u.is_superuser for u in users)
