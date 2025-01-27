from app.schemas import LoginRecordSchema, UserRegisterSchema


user_register_schema = UserRegisterSchema()
user_login_schema = UserRegisterSchema()

create_login_record_schema = LoginRecordSchema(only=('user_id', 'ip_address', 'user_agent'))