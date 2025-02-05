from marshmallow import Schema, fields, validate

from app.constants import ModelConstants, ValidationConstants
from app.utils import format_date, format_time


class BaseSchema(Schema):
    """Base schema with common fields."""

    id = fields.Int(dump_only=True)
    date = fields.Function(lambda obj: format_date(obj.created_at), dump_only=True)
    time = fields.Function(lambda obj: format_time(obj.created_at), dump_only=True)


class NameSchema(BaseSchema):
    """Base schema for models with name field."""

    name = fields.Str(
        required=True,
        validate=[
            validate.Length(
                min=ModelConstants.StringLength.MIN_NAME,
                max=ModelConstants.StringLength.MAX_NAME,
                error=ValidationConstants.Name.ERROR_MESSAGES['length']['general']
            ),
        ]
    )


class PersonSchema(BaseSchema):
    """Base schema for person-related models (Student, Teacher)."""

    first_name = fields.Str(
        required=True,
        validate=[
            validate.Length(
                min=ModelConstants.StringLength.MIN_FIRST_NAME,
                max=ModelConstants.StringLength.MAX_FIRST_NAME,
                error=ValidationConstants.Name.ERROR_MESSAGES['length']['first_name']
            )
        ]
    )

    last_name = fields.Str(
        required=True,
        validate=[
            validate.Length(
                min=ModelConstants.StringLength.MIN_LAST_NAME,
                max=ModelConstants.StringLength.MAX_LAST_NAME,
                error=ValidationConstants.Name.ERROR_MESSAGES['length']['last_name']
            )
        ]
    )

    phone = fields.Str(
        required=True,
        validate=validate.Regexp(
            ValidationConstants.Phone.PATTERN,
            error=ValidationConstants.Phone.ERROR_MESSAGES['pattern']
        )
    )

    email = fields.Email(
        required=True,
        validate=validate.Regexp(
            ValidationConstants.Email.PATTERN,
            error=ValidationConstants.Email.ERROR_MESSAGES['format']
        )
    )