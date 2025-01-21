"""
Authentication and User Management Schemas

This module contains all schemas related to user authentication and account management.
Each schema represents a specific authentication operation with its unique requirements:

Registration (UserRegisterSchema):
    - Email (required, validated format)
    - Password (required, strict validation)
    - Role (automatically set, defaults to student)

Login (UserLoginSchema):
    - Email (required)
    - Password (required, basic validation)
    - Remember me option (optional, defaults to False)

Password Management:
    - Forget Password (UserForgetPasswordSchema):
        Only requires email to send reset token
    - Reset Password (UserResetPasswordSchema):
        Requires email, reset token, and new password
    - Change Password (UserChangePasswordSchema):
        Requires current password verification and new password

Admin Management (UserAdminSchema):
    - Full user data access
    - Includes nested student/teacher data
    - Used for administrative operations
"""

from typing import Literal

from marshmallow import validate, fields, Schema

from app import ma
from app.constants import ValidationConstants, AuthConstants
from app.models import User
from app.schemas import BaseSchema


class BaseValidation:
    """
    Implements Factory Method pattern for generating marshmallow fields with consistent validation rules.

    This class provides class methods that serve as factory methods for creating
    pre-configured field instances. This pattern ensures:
    - Consistent validation rules across the application
    - DRY (Don't Repeat Yourself) by centralizing field configuration
    - Flexibility through kwargs for customization when needed

    Usage:
        email = BaseValidation.get_email_fields()
        password = BaseValidation.get_password_fields(validation_type='strict')
    """

    @classmethod
    def get_email_fields(cls, **kwargs) -> fields.Email:
        base_config = {
            "required": True,
            "validate": [
                validate.Email(),
                validate.Regexp(
                    ValidationConstants.Email.PATTERN,
                    error=ValidationConstants.Email.ERROR_MESSAGES['format']
                )
            ]
        }
        return fields.Email(**{**base_config, **kwargs})

    @classmethod
    def get_password_fields(cls, validation_type: Literal['strict', 'login'], **kwargs) -> fields.Str:
        base_config = {'required': True}

        if validation_type == 'strict':
            base_config['validate'] = [
                validate.Length(
                    min=ValidationConstants.Password.MIN_LENGTH,
                    error=ValidationConstants.Password.ERROR_MESSAGES['length']
                ),
                validate.Regexp(
                    ValidationConstants.Password.PATTERN,
                    error=ValidationConstants.Password.ERROR_MESSAGES['pattern']
                )
            ]
        elif validation_type == 'login':
            base_config['validate'] = validate.Length(
                min=1,
                error="Password cannot be empty"
            )

        return fields.Str(**{**base_config, **kwargs})


class UserBaseSchema(BaseSchema):
    email = BaseValidation.get_email_fields()


class UserRegisterSchema(ma.SQLAlchemyAutoSchema, UserBaseSchema):
    class Meta:
        model = User
        load_instance = True
        exclude = ("created_at", "id")

    password = BaseValidation.get_password_fields(validation_type='strict', load_only=True)
    role = fields.Str(
        dump_only=True,
        validate=validate.OneOf(AuthConstants.Role.CHOICES),
        default=AuthConstants.Role.STUDENT
    )


class UserLoginSchema(Schema):
    email = BaseValidation.get_email_fields()
    password = BaseValidation.get_password_fields(validation_type='login')
    remember = fields.Bool(missing=False)


class UserForgetPasswordSchema(UserBaseSchema):
    pass


class UserResetPasswordSchema(UserBaseSchema):
    token = fields.Str(
        required=True,
        validate=validate.Length(min=1, error="Token cannot be empty")
    )
    new_password = BaseValidation.get_password_fields(validation_type='strict')


class UserChangePasswordSchema(Schema):
    current_password = BaseValidation.get_password_fields(validation_type='strict')
    new_password = BaseValidation.get_password_fields(validation_type='strict')


class UserAdminSchema(ma.SQLAlchemyAutoSchema, BaseSchema):
    class Meta:
        model = User
        load_instance = True
        include_fk = True

    email = BaseValidation.get_email_fields()
    role = fields.Str(
        required=True,
        validate=validate.OneOf(AuthConstants.Role.CHOICES)
    )

    student = fields.Nested('StudentSchema', dump_only=True)
    teacher = fields.Nested('TeacherSchema', dump_only=True)


user_register_schema = UserRegisterSchema()
user_login_schema = UserLoginSchema()
user_forget_password_schema = UserForgetPasswordSchema()
user_reset_password_schema = UserResetPasswordSchema()
user_change_password_schema = UserChangePasswordSchema()
user_admin_schema = UserAdminSchema()
users_admin_schema = UserAdminSchema(many=True)