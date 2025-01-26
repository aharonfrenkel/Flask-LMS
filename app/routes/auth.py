from flask import Blueprint, Response

from app.factories import auth_service, user_login_schema
from app.middleware import validate_json_request, handle_exceptions
from app.utils import success_response


auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.post('/login')
@handle_exceptions
@validate_json_request(user_login_schema)
def login(data: dict) -> Response:
    user = auth_service.login_user(data)

    user_data = {
        'id': user.id,
        'email': user.email,
        'role': user.role
    }

    return success_response("Login successful", data=user_data)