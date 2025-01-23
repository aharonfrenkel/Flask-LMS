from app.factories import user_register_schema
from app.models import User
from app.factories import crud_service
from app.utils import hash_password


class AuthService:
    """
    Authentication service for user management.

    Handles user authentication operations:
    - Registration: Create new user accounts with validation
    - Login: Authenticate users and manage sessions
    - Logout: End user sessions securely
    - Password Management:
        * Forgot Password: Send reset tokens via email
        * Reset Password: Process password reset requests
        * Change Password: Update passwords for logged-in users
    """

    def register_user(self, data: dict) -> User:
        self._validate_email_not_taken(data['email'])
        user_data = self._prepare_user_data(data)
        return crud_service.create(user_data, user_register_schema)

    def _validate_email_not_taken(self, email: str) -> None:
        crud_service.validate_no_record_by_fields(
            model=User,
            error_msg=f"User with email: {email} already exists in the system",
            email=email
        )

    def _prepare_user_data(self, data: dict) -> dict:
        user_data = data.copy()
        user_data['password'] = hash_password(data['password'])
        return user_data