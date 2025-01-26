from functools import wraps
from typing import Any, Callable

from flask import request
from marshmallow import Schema
from werkzeug.exceptions import BadRequest


def validate_json_request(schema: Schema, partial: bool = False) -> Callable:
    """
    Validate JSON request data against a Marshmallow schema.

    Args:
        schema: Marshmallow schema for validation
        partial: Allow partial data validation for PATCH requests
    """
    def decorator(func) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            data = _validate_json_structure()
            _validate_json_schema(data, schema, partial)
            kwargs['data'] = data

            return func(*args, **kwargs)
        return wrapper
    return decorator

def _validate_json_structure() -> dict:
    """Validate JSON request structure and return data."""
    if not request.is_json:
        raise BadRequest("Content-Type must be application/json")

    data = request.get_json()

    if not data:
        raise BadRequest("Empty request body")

    return data

def _validate_json_schema(data: dict, schema: Schema, partial: bool) -> None:
    """Validate request data against schema."""
    schema.load(data, partial=partial)