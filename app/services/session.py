from flask import request
from werkzeug.exceptions import Conflict

from app.factories import crud_service, create_session_schema
from app.models import User, Session


class SessionService:
    def create_session(self, user: User) -> Session:
        """Create new session with client info."""
        self._validate_no_active_session(user)
        session_data = {
            'user_id': user.id,
            'ip_address': request.remote_addr,
            'user_agent': request.user_agent.string
        }
        return crud_service.create(session_data, create_session_schema)


    def _validate_no_active_session(self, user: User) -> None:
        """Check if user already has an active session from same client."""
        active_session = crud_service.find_one_by_fields(
            model=Session,
            user_id=user.id,
            ip_address=request.remote_addr,
            user_agent=request.user_agent.string,
            logout_time=None
        )

        if active_session and not active_session.is_expired:
            raise Conflict("User already has an active session")