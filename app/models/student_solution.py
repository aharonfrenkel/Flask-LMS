from sqlalchemy.sql import func

from app.constants import ModelConstants, GeneralConstants
from app.extensions import db
from app.models import BaseTable


class StudentSolution(BaseTable):
    """
    StudentSolution model representing a student's submission for an exercise.
    """

    # foreign keys
    student_id = db.Column(
        db.Integer,
        db.ForeignKey("student.id", ondelete="CASCADE"),
        nullable=False
    )

    exercise_id = db.Column(
        db.Integer,
        db.ForeignKey("exercise.id", ondelete="CASCADE"),
        nullable=False
    )

    # self columns
    content = db.Column(db.Text)

    submitted_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        server_default=func.current_timestamp()
    )

    status = db.Column(
        db.Enum(*GeneralConstants.Status.CHOICES),
        nullable=False,
        default=ModelConstants.DefaultValues.DEFAULT_STATUS
    )

    # relationships
    student = db.relationship(
        "Student",
        back_populates="solutions"
    )

    exercise = db.relationship(
        "Exercise",
        back_populates="student_solutions"
    )

    grade = db.relationship(
        "Grade",
        back_populates="solution",
        uselist=False,
        cascade="all, delete-orphan"
    )

    __table_args__ = (
        db.UniqueConstraint("student_id", "exercise_id", name="unique_student_exercise"),
    )