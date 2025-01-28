from datetime import datetime, timedelta

import pytz

from app import db
from app.constants import ModelConstants, GeneralConstants
from app.models import BaseTable


class Token(BaseTable):
    """
    Token model for password reset functionality.

    Attributes:
        user_id: Foreign key to User model
        token: Hashed reset token
        expiration: When token expires
        status: Token state (active/used/invalidated) - Controls token lifecycle:
                - active: Token is valid and can be used for password reset
                - used: Token has been successfully used for password reset
                - invalidated: Token was cancelled (e.g., due to new token creation)
    """

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False
    )

    token = db.Column(
        db.String(ModelConstants.StringLength.MAX_TOKEN),
        nullable=False,
        unique=True
    )

    expiration = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(pytz.utc) + timedelta(hours=GeneralConstants.Time.DEFAULT_TOKEN_EXPIRATION_HOURS)
    )

    status = db.Column(
        db.Enum(*ModelConstants.TokenStatus.CHOICES),
        nullable=False,
        default=ModelConstants.TokenStatus.ACTIVE
    )

    user = db.relationship("User", back_populates="tokens")