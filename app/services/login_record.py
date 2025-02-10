from flask import request

from app.models import User, LoginRecord
from app.schemas import LoginRecordSchema
from app.services import CRUDService


class LoginRecordService:
    """
    Service for managing login records.
    Handles the creation of audit logs for user login events.
    """
    def __init__(
            self,
            crud_service: CRUDService,
            create_login_record_schema: LoginRecordSchema
    ) -> None:
        self._crud_service = crud_service
        self._create_login_record_schema = create_login_record_schema

    def create_login_record(self, user: User) -> LoginRecord:
        """Create new login record with client info."""
        login_record_data = {
            'user_id': user.id,
            'ip_address': request.remote_addr,
            'user_agent': request.user_agent.string
        }
        return self._crud_service.create(login_record_data, self._create_login_record_schema)