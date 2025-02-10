from marshmallow import fields, validate

from app.extensions import ma
from app.constants import ModelConstants
from app.models import LoginRecord
from app.utils import format_date, format_time


class LoginRecordSchema(ma.SQLAlchemyAutoSchema):
    """Schema for login record data including timestamp and client info."""

    class Meta:
        model = LoginRecord
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

    login_date = fields.Function(
        lambda obj: format_date(obj.login_timestamp),
        dump_only=True
    )

    login_time = fields.Function(
        lambda obj: format_time(obj.login_timestamp),
        dump_only=True
    )

    ip_address = fields.IP()

    user_agent = fields.Str(
        validate=validate.Length(max=ModelConstants.StringLength.MAX_USER_AGENT)
    )

    user = fields.Nested(
        'UserAdminSchema',
        dump_only=True,
        only=('email', 'role')
    )