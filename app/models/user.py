from flask_login import UserMixin

from app import db
from app.constants import ModelConstants, AuthConstants
from app.models import BaseTable


class User(BaseTable, UserMixin):
    """
    User account model.

    Attributes:
        email: User's email address (used for login)
        password: Hashed password
        role: User's role (admin, teacher, or student)
        student: One-to-one relationship with Student model
        teacher: One-to-one relationship with Teacher model
        sessions: One-to-many relationship with Session model
    """

    # self columns
    email = db.Column(
        db.String(ModelConstants.StringLength.MAX_EMAIL),
        nullable=False,
        unique=True
    )

    password = db.Column(
        db.String(ModelConstants.StringLength.MAX_PASSWORD),
        nullable=False
    )

    role = db.Column(
        db.Enum(*AuthConstants.Role.CHOICES),
        nullable=False,
        default="student"
    )

    # relationships
    student = db.relationship(
        "Student",
        back_populates="user",
        uselist=False
    )

    teacher = db.relationship(
        "Teacher",
        back_populates="user",
        uselist=False
    )

    sessions = db.relationship(
        "Session",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    token = db.relationship(
        "Token",
        back_populates="user",
        cascade = "all, delete-orphan",
        uselist=False
    )

    def get_id(self) -> str:
        """Required by Flask-Login."""
        return str(self.id)

    @property
    def is_admin(self) -> bool:
        """Check if user is an admin."""
        return self.role == AuthConstants.Role.ADMIN

    @property
    def is_teacher(self) -> bool:
        """Check if user is a teacher."""
        return self.role == AuthConstants.Role.TEACHER

    @property
    def is_student(self) -> bool:
        """Check if user is a student."""
        return self.role == AuthConstants.Role.STUDENT