from app.schemas import (
    LoginRecordSchema,
    UserRegisterSchema,
    UserLoginSchema,
    UserForgetPasswordSchema,
    TokenSchema,
    UserResetPasswordSchema,
    UserChangePasswordSchema
)


user_register_schema = UserRegisterSchema()
user_login_schema = UserLoginSchema()
user_forgot_password_schema = UserForgetPasswordSchema()
user_reset_password_schema = UserResetPasswordSchema()
user_change_password_schema = UserChangePasswordSchema()


create_login_record_schema = LoginRecordSchema(only=('user_id', 'ip_address', 'user_agent'))
create_token_schema = TokenSchema()