from flask import Blueprint, Response
from flask_login import login_required

from app.factories import (
    auth_service,
    user_login_schema,
    user_forgot_password_schema,
    user_reset_password_schema,
    user_update_password_schema, user_public_schema
)
from app.middleware import validate_json_request, handle_exceptions, logout_required
from app.utils import success_response


auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.post('/login')
@handle_exceptions
@logout_required
@validate_json_request(user_login_schema)
def login(data: dict) -> Response:
    user = auth_service.login_user(data)

    return success_response(
        "Login successful",
        data=user,
        schema=user_public_schema
    )


@auth_bp.post('/logout')
@handle_exceptions
@login_required
def logout() -> Response:
    auth_service.logout_user()

    return success_response("Logout successful")


@auth_bp.post('/password/forgot')
@handle_exceptions
@logout_required
@validate_json_request(user_forgot_password_schema)
def forgot_password(data: dict) -> Response:
    auth_service.forgot_password(data)

    return success_response("Reset password sent. Check your email.")


@auth_bp.post('/password/reset')
@handle_exceptions
@logout_required
@validate_json_request(user_reset_password_schema)
def reset_password(data: dict) -> Response:
    auth_service.reset_password(data)

    return success_response("Password reset successful")


@auth_bp.post('/password/update')
@handle_exceptions
@login_required
@validate_json_request(user_update_password_schema)
def update_password(data: dict) -> Response:
    auth_service.update_password(data)

    return success_response("Password updated successful")