"""
Authentication and User Management Schemas

This module contains all schemas related to user authentication and account management.
Each schema represents a specific authentication operation with its unique requirements:

Registration (UserRegisterSchema):
    - Email (required, validated format)
    - Password (required, strict validation)
    - Role (automatically set, defaults to student)

Login (LoginRequestSchema):
    - Email (required)
    - Password (required, basic validation)
    - Remember me option (optional, defaults to False)

Password Management:
    - Forget Password (ForgetPasswordRequestSchema):
        Only requires email to send reset token
    - Reset Password (ResetPasswordRequestSchema):
        Requires email, reset token, and new password
    - Change Password (UpdatePasswordRequestSchema):
        Requires current password verification and new password
"""

from typing import Literal

from marshmallow import validate, fields, Schema

from app.extensions import ma
from app.constants import ValidationConstants, AuthConstants
from app.models import User


__all__ = [
    'UserRegisterSchema',
    'LoginRequestSchema',
    'ForgetPasswordRequestSchema',
    'ResetPasswordRequestSchema',
    'UpdatePasswordRequestSchema'
]


class BaseValidation:
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
    def get_password_fields(cls, validation_type: Literal['strict', 'lenient'], **kwargs) -> fields.Str:
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
        else:
            base_config['validate'] = validate.Length(
                min=1,
                error="cannot be empty"
            )

        return fields.Str(**{**base_config, **kwargs})


class UserBaseSchema(Schema):
    email = BaseValidation.get_email_fields()


class UserRegisterSchema(ma.SQLAlchemyAutoSchema, UserBaseSchema):
    class Meta:
        model = User
        load_instance = True
        exclude = ('id', 'created_at')

    password = BaseValidation.get_password_fields(validation_type='strict', load_only=True)
    role = fields.Str(
        validate=validate.OneOf(AuthConstants.Role.CHOICES),
        missing=AuthConstants.Role.STUDENT
    )


class LoginRequestSchema(UserBaseSchema):
    password = BaseValidation.get_password_fields(validation_type='lenient')
    remember = fields.Bool(missing=False)


class ForgetPasswordRequestSchema(UserBaseSchema):
    pass


class ResetPasswordRequestSchema(UserBaseSchema):
    token = BaseValidation.get_password_fields(validation_type='lenient')
    new_password = BaseValidation.get_password_fields(validation_type='strict')


class UpdatePasswordRequestSchema(Schema):
    current_password = BaseValidation.get_password_fields(validation_type='lenient')
    new_password = BaseValidation.get_password_fields(validation_type='strict')