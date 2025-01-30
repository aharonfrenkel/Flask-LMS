from app.services.db import DatabaseService
from app.services.crud import CRUDService
from app.services.auth import AuthService
from app.services.login_record import LoginRecordService
from app.services.token import TokenService
from app.services.email import EmailService
from app.services.user import UserService
from .schema_factories import create_login_record_schema, user_register_schema, create_token_schema


db_service = DatabaseService()
crud_service = CRUDService(db_service)
login_record_service = LoginRecordService(crud_service, create_login_record_schema)
token_service = TokenService(crud_service, create_token_schema)
email_service = EmailService()
user_service = UserService(crud_service)
auth_service = AuthService(
    db_service,
    crud_service,
    user_service,
    token_service,
    login_record_service,
    email_service,
    user_register_schema
)