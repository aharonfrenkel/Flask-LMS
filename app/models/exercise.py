from datetime import datetime, timedelta

import pytz

from app.constants import GeneralConstants
from app.extensions import db
from app.models import NameMixin


class Exercise(NameMixin):
    """
    Exercise model representing course assignments and tasks.

    Inherits from NameMixin which provides:
    - name field with validation

    Each exercise is associated with a lecture and can have multiple student solutions.
    Includes deadline management and submission tracking.
    """

    # foreign keys
    lecture_id = db.Column(
        db.Integer,
        db.ForeignKey("lecture.id", ondelete="CASCADE"),
        nullable=False
    )

    teacher_id = db.Column(
        db.Integer,
        db.ForeignKey("teacher.id", ondelete="SET NULL")
    )

    # self columns
    content = db.Column(
        db.Text,
        nullable=False
    )

    target_date = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(pytz.utc) + timedelta(GeneralConstants.Time.DEFAULT_EXERCISE_TARGET_DAYS)
    )

    is_mandatory = db.Column(
        db.Boolean,
        default=True
    )

    teacher_solution = db.Column(db.Text)

    # relationship
    lecture = db.relationship(
        "Lecture",
        back_populates="exercises"
    )

    teacher = db.relationship(
        "Teacher",
        back_populates="exercises"
    )

    student_solutions = db.relationship(
        "StudentSolution",
        back_populates="exercise",
        cascade="all, delete-orphan"
    )

    __table_args__ = (
        db.UniqueConstraint("name", "lecture_id", name="unique_exercise"),
    )