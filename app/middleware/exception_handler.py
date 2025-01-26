from functools import wraps
from http import HTTPStatus
from typing import Callable

from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import BadRequest, Unauthorized, Forbidden, NotFound, Conflict, InternalServerError

from app.utils import error_response


def handle_exceptions(func) -> Callable:
    """
    A decorator for handling common HTTP exceptions.

    Handles:
    - BadRequest (400): Invalid request data
    - Unauthorized (401): Authentication required
    - Forbidden (403): Insufficient permissions
    - NotFound (404): Resource not found
    - Conflict (409): Resource conflict
    - ValidationError (422): Schema validation error
    - SQLAlchemyError (500): Internal server error
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except BadRequest as err:
            return error_response(err.description, HTTPStatus.BAD_REQUEST)
        except Unauthorized as err:
            return error_response(err.description, HTTPStatus.UNAUTHORIZED)
        except Forbidden as err:
            return error_response(err.description, HTTPStatus.FORBIDDEN)
        except NotFound as err:
            return error_response(err.description, HTTPStatus.NOT_FOUND)
        except Conflict as err:
            return error_response(err.description, HTTPStatus.CONFLICT)
        except ValidationError as err:
            return error_response(err.messages, HTTPStatus.UNPROCESSABLE_ENTITY)
        except SQLAlchemyError as err:
            return error_response(str(err), HTTPStatus.INTERNAL_SERVER_ERROR)
        except InternalServerError as err:
            return error_response(str(err), HTTPStatus.INTERNAL_SERVER_ERROR)

    return wrapper