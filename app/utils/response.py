from http import HTTPStatus
from typing import Any


def success_response(
        message: str = "Operation completed successfully",
        data: Any | None = None,
        schema: Any | None = None,
        status_code: HTTPStatus = HTTPStatus.OK
) -> tuple[dict, HTTPStatus]:
    """Create successful API response."""
    response_data = {
        'success': True,
        'message': message
    }

    if data:
        response_data['data'] = schema.dump(data) if schema else data

    return response_data, status_code


def error_response(
        message: str = "Operation failed",
        status_code: HTTPStatus = HTTPStatus.BAD_REQUEST
) -> tuple[dict, HTTPStatus]:
    """Create error API response."""
    response_data = {
        'success': False,
        'message': message
    }

    return response_data, status_code