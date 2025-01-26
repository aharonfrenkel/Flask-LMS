from marshmallow import fields, validate

from app import ma
from app.constants import ModelConstants
from app.models import Session
from app.utils import format_date, format_time


class SessionSchema(ma.SQLAlchemyAutoSchema):
    """Schema for user session data including login/logout times and client info."""

    class Meta:
        model = Session
        load_instance = True
        exclude = ('date', 'time')

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
        lambda obj: format_date(obj.login_time),
        dump_only=True
    )

    login_time = fields.Function(
        lambda obj: format_time(obj.login_time),
        dump_only=True
    )

    logout_date = fields.Function(
        lambda obj: format_date(obj.logout_time) if obj.logout_time else None,
        dump_only=True
    )

    logout_time = fields.Function(
        lambda obj: format_time(obj.logout_time) if obj.logout_time else None,
        dump_only=True
    )

    last_activity_date = fields.Function(
        lambda obj: format_date(obj.last_activity),
        dump_only=True
    )

    last_activity_time = fields.Function(
        lambda obj: format_time(obj.last_activity),
        dump_only=True
    )

    ip_address = fields.IP(
        validate=validate.Length(max=ModelConstants.StringLength.MAX_IP_ADDRESS)
    )

    user_agent = fields.Str(
        validate=validate.Length(max=ModelConstants.StringLength.MAX_USER_AGENT)
    )

    user = fields.Nested(
        'UserAdminSchema',
        dump_only=True,
        only=('email', 'role')
    )