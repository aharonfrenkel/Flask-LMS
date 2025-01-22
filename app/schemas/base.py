from marshmallow import Schema, fields, validate

from app.constants import ModelConstants, ValidationConstants


class BaseSchema(Schema):
    """Base schema with common fields."""

    id = fields.Int(dump_only=True)
    date = fields.Method("get_date", dump_only=True)
    time = fields.Method("get_time", dump_only=True)

    def get_date(self, obj):
        return obj.created_at.strftime("%d-%m-%Y")

    def get_time(self, obj):
        return obj.created_at.strftime("%H:%M:%S")


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