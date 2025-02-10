from flask_login import current_user, login_user, logout_user
from werkzeug.exceptions import Unauthorized

from app.constants import ValidationConstants
from app.models import User
from app.schemas import UserRegisterSchema
from app.services.crud import CRUDService
from app.services.db import DatabaseService
from app.services.email import EmailService
from app.services.login_record import LoginRecordService
from app.services.token import TokenService
from app.services.user import UserService
from app.utils import hash_password, verify_password


class AuthService:
    """
    Authentication service for user management.

    Handles user authentication operations:
    - Registration: Create new user accounts with validation
    - Login: Authenticate users and record login events
    - Logout: End user authentication session via Flask-Login
    - Password Management:
        * Forgot Password: Send reset tokens via email
        * Reset Password: Process password reset requests
        * Change Password: Update passwords for logged-in users
    """
    def __init__(
            self,
            db_service: DatabaseService,
            crud_service: CRUDService,
            user_service: UserService,
            token_service: TokenService,
            login_record_service: LoginRecordService,
            email_service: EmailService,
            user_register_schema: UserRegisterSchema
    ) -> None:
        self._db_service = db_service
        self._crud_service = crud_service
        self._user_service = user_service
        self._token_service = token_service
        self._login_record_service = login_record_service
        self._email_service = email_service
        self._user_register_schema = user_register_schema

    # Registration service
    def register_user(self, data: dict) -> User:
        """
        Register a new user account.

        Args:
            data: Dict with 'email', 'password' and optional 'role'

        Returns:
            User: The newly created user object

        Raises:
            Conflict: If email already exists
        """
        self._user_service.validate_email_not_taken(data['email'])
        user_data = self._prepare_user_data(data)
        return self._crud_service.create(user_data, self._user_register_schema)

    def _prepare_user_data(self, data: dict) -> dict:
        user_data = data.copy()
        user_data['password'] = hash_password(data['password'])
        return user_data


    # Login service
    def login_user(self, data: dict) -> User:
        """
        Authenticate user and create login record.

        Args:
            data: Dict with 'email', 'password' and optional 'remember' flag

        Raises:
            Unauthorized: For any authentication failure, with generic message
            to prevent user enumeration attacks.
        """
        user = self._authenticate_user(data)
        self._login_record_service.create_login_record(user)
        login_user(user, remember=data.get('remember', False))
        return user

    def _authenticate_user(self, data: dict) -> User:
        user = self._user_service.find_by_email_or_raise(
            data['email'],
            exception=Unauthorized,
            error_msg="Invalid email or password"
        )

        if not verify_password(user.password, data['password']):
            raise Unauthorized("Invalid email or password")

        return user


    # Logout service
    def logout_user(self) -> None:
        """End user's authenticated session using Flask-Login."""
        logout_user()


    # Forgot password service
    def forgot_password(self, data: dict) -> None:
        """
        Send password reset token to user's email address.

        Args:
            data: Dict with 'email'
        Note:
            Does not raise exceptions for non-existent emails
            as part of security measures against user enumeration.
            Always processes silently regardless of email existence.
        """
        user = self._user_service.find_by_email(data['email'])

        if user:
            reset_token = self._token_service.create_password_reset_token(user)
            self._email_service.send_password_reset_token(user.email, reset_token)


    # Reset password service
    def reset_password(self, data: dict) -> None:
        """
        Reset user's password using a valid reset token.

        Args:
            data: Dict with 'email', 'token', and 'new_password'

        Raises:
            Unauthorized: For any validation failure, with generic message
            to prevent user enumeration attacks.
        """
        user = self._user_service.find_by_email_or_raise(
            data['email'],
            exception=Unauthorized,
            error_msg=ValidationConstants.ResetPassword.ERROR_MESSAGES['general_error']
        )
        with self._db_service.transaction():
            self._token_service.mark_token_as_used(user, data['token'])
            self._user_service.update_user_password(user, data['new_password'])
        self._email_service.send_password_reset_confirmation(user.email)


    # Update password service
    def update_password(self, data: dict) -> None:
        """
        Update user's password.

        Args:
            data: Dict with 'current_password' and 'new_password'
        """
        if not verify_password(current_user.password, data['current_password']):
            raise Unauthorized("Current password is incorrect")
        self._user_service.update_user_password(current_user, data['new_password'])