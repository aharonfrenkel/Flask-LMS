from http import HTTPStatus
from typing import Any

from flask import jsonify


def success_response(
        message: str = "Operation completed successfully",
        data: Any | None = None,
        status_code: HTTPStatus = HTTPStatus.OK
) -> tuple[jsonify, HTTPStatus]:
    """Create successful API response."""
    response_data = {
        'success': True,
        'message': message
    }

    if data is not None:
        response_data['data'] = data

    return jsonify(response_data), status_code


def error_response(
        message: str = "Operation failed",
        status_code: HTTPStatus = HTTPStatus.BAD_REQUEST
) -> tuple[jsonify, HTTPStatus]:
    """Create error API response."""
    response_data = {
        'success': False,
        'message': message
    }

    return jsonify(response_data), status_code