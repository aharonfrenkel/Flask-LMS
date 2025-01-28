from flask_login import login_user, logout_user
from werkzeug.exceptions import Unauthorized

from app.models import User
from app.schemas import UserRegisterSchema
from app.services.crud import CRUDService
from app.services.login_record import LoginRecordService
from app.services.token import TokenService
from app.services.email import EmailService
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
            crud_service: CRUDService,
            login_record_service: LoginRecordService,
            user_register_schema: UserRegisterSchema,
            token_service: TokenService,
            email_service: EmailService
    ) -> None:
        self._crud_service = crud_service
        self._login_record_service = login_record_service
        self._user_register_schema = user_register_schema
        self._token_service = token_service
        self._email_service = email_service

    # Registration service
    def register_user(self, data: dict) -> User:
        """
        Register a new user account.

        Args:
            data: Dict with 'email', 'password' and optional 'role'

        Raises:
            Conflict: If email already exists
        """
        self._validate_email_not_taken(data['email'])
        user_data = self._prepare_user_data(data)
        return self._crud_service.create(user_data, self._user_register_schema)

    def _validate_email_not_taken(self, email: str) -> None:
        self._crud_service.validate_no_record_by_fields(
            model=User,
            error_msg=f"User with email: {email} already exists in the system",
            email=email
        )

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
        user = self._crud_service.find_one_by_fields_or_raise(
            model=User,
            exception=Unauthorized,
            error_msg="Invalid email or password",
            email=data['email']
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
        user = self._find_user_by_email(data['email'])

        if user:
            reseet_token = self._token_service.create_password_reset_token(user)
            self._email_service.send_password_reset_email(user.email, reseet_token)

    def _find_user_by_email(self, email: str) -> User:
        return self._crud_service.find_one_by_fields(
            model=User,
            email=email
        )