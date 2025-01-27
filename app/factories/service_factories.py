from app.services import CRUDService, DatabaseService, AuthService, LoginRecordService
from .schema_factories import create_login_record_schema, user_register_schema

db_service = DatabaseService()
crud_service = CRUDService(db_service)
login_record_service = LoginRecordService(crud_service, create_login_record_schema)
auth_service = AuthService(crud_service, login_record_service, user_register_schema)