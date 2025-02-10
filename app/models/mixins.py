from sqlalchemy.orm import declared_attr

from app.extensions import db
from app.constants import ModelConstants
from app.models import BaseTable


class NameMixin(BaseTable):
    """
    Mixin for models that have a name field.

    Adds:
    - name field with length validation
    """

    __abstract__ = True

    name = db.Column(
        db.String(ModelConstants.StringLength.MAX_NAME),
        nullable=False
    )

    @declared_attr
    def __table_args__(cls):
        return (
            db.CheckConstraint(
                f"length(name) >= {ModelConstants.StringLength.MIN_NAME}",
                name=f"{cls.__tablename__}name_length"
            ),
        )


class PersonMixin(BaseTable):
    """
    Mixin for models representing people (students, teachers).

    Adds:
    - Basic personal information fields
    - User relationship
    - Field validation constraints
    """

    __abstract__ = True

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id", ondelete="SET NULL"),
        unique=True
    )

    first_name = db.Column(
        db.String(ModelConstants.StringLength.MAX_FIRST_NAME),
        nullable=False
    )

    last_name = db.Column(
        db.String(ModelConstants.StringLength.MAX_LAST_NAME),
        nullable=False
    )

    phone = db.Column(
        db.String(ModelConstants.StringLength.EQUAL_PHONE),
        unique=True
    )

    email = db.Column(
        db.String(ModelConstants.StringLength.MAX_EMAIL),
        nullable=False,
        unique=True
    )

    @declared_attr
    def user(cls):
        """Relationship to User model."""
        return db.relationship(
            "User",
            back_populates=f"{cls.__tablename__}"
        )

    @declared_attr
    def __table_args__(cls):
        return (
            db.CheckConstraint(
                f"length(first_name) >= {ModelConstants.StringLength.MIN_FIRST_NAME}",
                name=f"{cls.__tablename__}_first_name_length"
            ),
            db.CheckConstraint(
                f"length(last_name) >= {ModelConstants.StringLength.MIN_LAST_NAME}",
                name=f"{cls.__tablename__}_last_name_length"
            ),
            db.CheckConstraint(
                f"length(phone) = {ModelConstants.StringLength.EQUAL_PHONE}",
                name=f"{cls.__tablename__}_phone_length"
            ),
        )

    @property
    def full_name(self):
        """Get person's full name."""
        return f"{self.first_name} {self.last_name}"