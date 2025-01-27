from flask import request

from app.factories import crud_service, create_login_record_schema
from app.models import User, LoginRecord


class LoginRecordService:
    """
    Service for managing login records.
    Handles the creation of audit logs for user login events.
    """
    def create_login_record(self, user: User) -> LoginRecord:
        """Create new login record with client info."""
        login_record_data = {
            'user_id': user.id,
            'ip_address': request.remote_addr,
            'user_agent': request.user_agent.string
        }
        return crud_service.create(login_record_data, create_login_record_schema)