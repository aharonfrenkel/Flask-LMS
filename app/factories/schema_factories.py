from app.schemas import LoginRecordSchema, UserRegisterSchema, UserLoginSchema, UserForgetPasswordSchema, TokenSchema

user_register_schema = UserRegisterSchema()
user_login_schema = UserLoginSchema()
user_forgot_password_schema = UserForgetPasswordSchema()

create_login_record_schema = LoginRecordSchema(only=('user_id', 'ip_address', 'user_agent'))
create_token_schema = TokenSchema()