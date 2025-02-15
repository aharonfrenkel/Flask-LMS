from sqlalchemy.orm import declared_attr
from sqlalchemy.sql import func

from app.extensions import db
from app.utils import camelcase_to_snakecase


class BaseTable(db.Model):
    """
    Abstract base class for all database models.

    Provides:
    - Automatic table naming based on class name (CamelCase to snake_case)
    - Primary key (id)
    - Creation timestamp with timezone
    """

    __abstract__ = True

    @declared_attr
    def __tablename__(cls):
        """Generate table name from class name (e.g., UserProfile -> user_profile)."""
        return camelcase_to_snakecase(cls.__name__).lower()

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        server_default=func.current_timestamp()
    )