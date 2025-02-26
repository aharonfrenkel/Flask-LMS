from app.schemas import (
    LoginRecordSchema,
    UserRegisterSchema,
    UserLoginSchema,
    UserForgetPasswordSchema,
    TokenSchema,
    UserResetPasswordSchema,
    UserUpdatePasswordSchema,
    CourseWriteSchema,
    CourseReadSchema,
    CourseAdminSchema
)


user_register_schema = UserRegisterSchema()
user_login_schema = UserLoginSchema()
user_forgot_password_schema = UserForgetPasswordSchema()
user_reset_password_schema = UserResetPasswordSchema()
user_update_password_schema = UserUpdatePasswordSchema()


create_login_record_schema = LoginRecordSchema(only=('user_id', 'ip_address', 'user_agent'))
create_token_schema = TokenSchema()


course_write_schema = CourseWriteSchema()
course_read_schema = CourseReadSchema()
course_admin_schema = CourseAdminSchema()

course_read_list_schema = CourseReadSchema(many=True)
course_admin_list_schema = CourseAdminSchema(many=True)