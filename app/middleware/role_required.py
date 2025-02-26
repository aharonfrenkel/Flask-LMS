from functools import wraps

from flask_login import current_user
from werkzeug.exceptions import Forbidden


def role_required(*allowed_roles):
    """
    Decorator to restrict endpoint access to specific roles.

    Args:
        allowed_roles: List of roles that can access the endpoint

    Raises:
        Forbidden: If the current user's role is not in the list of allowed roles
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if current_user.role not in allowed_roles:
                raise Forbidden("You don't have permission to access this resource")
            return func(*args, **kwargs)
        return wrapper
    return decorator