from app.modules.users.repositories.user_repository import UserRepository
from app.modules.users.schemas import UserCreate, UserUpdate, UserAllowedUpdate, UserAllowedCreate
from app.modules.users.models import User
from app.core.exceptions import NotFoundException, ConflictException
from app.core.security import hash_password
import pyotp
from app.core.security import encrypt
from app.utils.send_mail import send_mail
from app.api.schemas.mail import EmailSchema, EmailTemplate
import json
from datetime import datetime, timedelta
from app.modules.notifications.repositories.notification_repository import NotificationRepository
from app.modules.notifications.models import Notification

class UserService:
    def __init__(
        self,
        repository: UserRepository,
        notification_repository: NotificationRepository,
    ):
        self.repository = repository
        self.notification_repository = notification_repository

    async def email_verification(self, user: User):
        expiration = datetime.now() + timedelta(hours=24)
        code = encrypt(
            json.dumps(
                {
                    "email": user.email,
                    "expiration": expiration.timestamp(),
                    "type": "email_verification",
                }
            ),
        )

        message = {
            "name": user.name,
            "code": code[8:],
        }

        self.notification_repository.create(
            Notification(
                message=message,
                user_id=user.id,
            )
        )
        
        await send_mail(
            EmailSchema(
                recipients=[user.email],
                subject="Email Verification",
                template_body=message,
                template=EmailTemplate.EMAIL_VERIFICATION,
            )
        )

    async def create_user(self, data: UserCreate | UserAllowedCreate, email_validate: bool = False) -> User:
        user = User.model_validate(data)

        _,existing = self.repository.list({"email": user.email})
        if existing:
            raise ConflictException("Email already registered.")

        hashed_password = hash_password(user.password)
        two_factor_secret = pyotp.random_base32()

        user.password = hashed_password
        user.two_factor_secret = encrypt(two_factor_secret)

        if user.is_active:
            user.is_active = not email_validate

        user = self.repository.create(user)

        if email_validate:
            await self.email_verification(user)

        return user

    def get_user(self, user_id: int) -> User:
        user = self.repository.get(user_id)
        if not user:
            raise NotFoundException("User not found.")
        return user

    def list_users(self, **filters) -> tuple[list[User], int]:
        return self.repository.list(filters)

    def update_user(self, user_id: int, data: UserUpdate | UserAllowedUpdate) -> User:
        user = self.repository.get(user_id)
        if not user:
            raise NotFoundException("User not found.")

        if data.email and data.email != user.email:
            _,existing = self.repository.list({"email": data.email})
            if existing:
                raise ConflictException("Email already registered.")
            
        update_data = data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            if value is not None:
                setattr(user, key, value)

        if data.password is not None:
            user.password = hash_password(data.password)

        return self.repository.update(user)

    def delete_user(self, user_id: int) -> None:
        user = self.repository.get(user_id)
        if not user:
            raise NotFoundException("User not found.")

        user.is_active = False
        self.repository.update(user)

        return None

    def hard_delete_user(self, user_id: int) -> None:
        user = self.repository.get(user_id)
        if not user:
            raise NotFoundException("User not found.")

        self.repository.delete(user)

        return None
