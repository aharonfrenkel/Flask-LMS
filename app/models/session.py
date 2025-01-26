from datetime import datetime, timedelta

import pytz
from sqlalchemy import func

from app import db
from app.constants import ModelConstants, GeneralConstants
from app.models import BaseTable


class Session(BaseTable):
    """
    Session model for tracking user login sessions.

    This model maintains user session information including login/logout times,
    last activity, and client details. It helps manage user sessions and implement
    security features like session expiration and device tracking.

    Attributes:
        user_id (int): Foreign key to User model
        login_time (datetime): When the session started
        logout_time (datetime): When the session ended (None if still active)
        last_activity (datetime): Last recorded user activity
        ip_address (str): Client's IP address
        user_agent (str): Client's browser/device information
        user (User): Relationship to the User model
    """

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )

    login_time = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        server_default=func.current_timestamp()
    )

    logout_time = db.Column(db.DateTime(timezone=True))

    last_activity = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        server_default=func.current_timestamp()
    )

    ip_address = db.Column(db.String(ModelConstants.StringLength.MAX_IP_ADDRESS))

    user_agent = db.Column(db.String(ModelConstants.StringLength.MAX_USER_AGENT))

    user = db.relationship("User", back_populates="sessions")

    @property
    def is_expired(self) -> bool:
        """Check if session has expired based on last activity."""
        max_lifetime = timedelta(weeks=GeneralConstants.Time.DEFAULT_SESSION_LIFETIME_WEEKS)
        current_time = datetime.now(pytz.utc)

        return current_time - self.last_activity > max_lifetime

    def update_activity(self) -> None:
        self.last_activity = func.current_timestamp()

    def end_session(self):
        self.logout_time = datetime.now(pytz.utc)
        self.last_activity = datetime.now(pytz.utc)