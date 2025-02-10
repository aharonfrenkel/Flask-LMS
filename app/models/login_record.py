from sqlalchemy import func

from app.extensions import db
from app.constants import ModelConstants
from app.models import BaseTable


class LoginRecord(BaseTable):
    """
    Records user login events for auditing and monitoring purposes.
    Tracks important login metadata.

    Attributes:
        user_id (int): Foreign key to User model
        login_timestamp (datetime): When the login occurred
        ip_address (str): Client's IP address
        user_agent (str): Client's browser/device information
        user (User): Relationship to the User model
    """

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False
    )

    login_timestamp = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        server_default=func.current_timestamp()
    )

    ip_address = db.Column(db.String(ModelConstants.StringLength.MAX_IP_ADDRESS))

    user_agent = db.Column(db.String(ModelConstants.StringLength.MAX_USER_AGENT))

    user = db.relationship("User", back_populates="login_records")