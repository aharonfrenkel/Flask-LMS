from flask_login import login_user
from werkzeug.exceptions import Unauthorized

from app.models import User
from app.schemas import UserRegisterSchema
from app.services import CRUDService, LoginRecordService
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
            user_register_schema: UserRegisterSchema
    ) -> None:
        self._crud_service = crud_service
        self._login_record_service = login_record_service
        self._user_register_schema = user_register_schema

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