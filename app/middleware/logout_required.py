from functools import wraps
from typing import Callable

from flask_login import current_user
from werkzeug.exceptions import Forbidden


def logout_required(func) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        if current_user.is_authenticated:
            raise Forbidden("This endpoint is only available for non-authenticated users")
        return func(*args, **kwargs)
    return wrapper