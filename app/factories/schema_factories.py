from app.schemas import LoginRecordSchema, UserRegisterSchema, UserLoginSchema


user_register_schema = UserRegisterSchema()
user_login_schema = UserLoginSchema()

create_login_record_schema = LoginRecordSchema(only=('user_id', 'ip_address', 'user_agent'))