from sqlalchemy.sql import func

from app.constants import ModelConstants, GeneralConstants
from app.extensions import db
from app.models import BaseTable


class StudentSolution(BaseTable):
    """
    StudentSolution model representing a student's submission for an exercise.
    """

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

    content = db.Column(db.Text)

    submitted_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        server_default=func.current_timestamp()
    )

    status = db.Column(
        db.String(ModelConstants.StringLength.MAX_STATUS),
        nullable=False,
        default=ModelConstants.DefaultValues.DEFAULT_STATUS
    )

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
        db.CheckConstraint(
            f"status IN {GeneralConstants.Status.CHOICES}",
            name="valid_status"
        ),
        db.UniqueConstraint("student_id", "exercise_id", name="unique_student_exercise"),
    )