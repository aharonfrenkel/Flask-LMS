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
        is_used: Whether token has been used
        expiration: When token expires
    """

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
        unique=True
    )

    token = db.Column(
        db.String(ModelConstants.StringLength.MAX_TOKEN),
        nullable=False,
        unique=True
    )

    is_used = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )

    expiration = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(pytz.utc) + timedelta(hours=GeneralConstants.Time.DEFAULT_TOKEN_EXPIRATION_HOURS)
    )

    user = db.relationship("User", back_populates="token")

    def __init__(self, user_id: int, token: str):
        self.user_id = user_id
        self.token = token