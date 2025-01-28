from marshmallow import fields, validate

from app import ma
from app.constants import ModelConstants
from app.models import Token


class TokenSchema(ma.SQLAlchemyAutoSchema):
    """Schema for password reset tokens."""

    class Meta:
        model = Token
        load_instance = True

    user_id = fields.Int(
        required=True,
        validate=[
            validate.Range(
                min=1,
                error="User ID must be positive"
            )
        ]
    )

    token = fields.Str(
        required=True,
        load_only=True
    )

    expiration = fields.DateTime(dump_only=True)

    status = fields.Str(
        validate=[
            validate.OneOf(
                ModelConstants.TokenStatus.CHOICES,
                error=f"Status must be one of {ModelConstants.TokenStatus.CHOICES}"
            )
        ],
        missing=ModelConstants.TokenStatus.ACTIVE
    )