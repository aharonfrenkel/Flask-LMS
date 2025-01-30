from typing import Optional, Type


from app.models import User
from app.services import CRUDService
from app.utils import hash_password


class UserService:
    """
    Service for managing user-related operations.

    Provides centralized user management functionality including:
    - User lookup and validation
    - Email availability checking
    - Password management and security

    This service acts as a domain-specific wrapper around basic CRUD operations,
    adding business logic and validation specific to user management.
    """

    def __init__(self, crud_service: CRUDService) -> None:
        self._crud_service = crud_service

    def find_by_email(self, email: str) -> Optional[User]:
        return self._crud_service.find_one_by_fields(
            model=User,
            email=email
        )

    def find_by_email_or_raise(
            self,
            email: str,
            exception: Type[Exception],
            error_msg: str
    ) -> User:
        return self._crud_service.find_one_by_fields_or_raise(
            model=User,
            exception=exception,
            error_msg=error_msg,
            email=email
        )

    def validate_email_not_taken(self, email: str) -> None:
        self._crud_service.validate_no_record_by_fields(
            model=User,
            error_msg=f"User with email: {email} already exists",
            email=email
        )

    def update_user_password(self, user: User, password: str) -> None:
        self._crud_service.update(
            user,
            {'password': hash_password(password)}
        )