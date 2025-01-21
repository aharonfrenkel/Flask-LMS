from app.constants import ModelConstants, GeneralConstants
from app.extensions import db
from app.models import BaseTable


class Grade(BaseTable):
    """
    Grade model for storing assessment information.

    Separating grades into their own table provides:
    1. Better normalization
    2. Easier grade history tracking
    3. Cleaner separation of concerns
    4. More flexible grading schemes
    """

    # foreign keys
    solution_id = db.Column(
        db.Integer,
        db.ForeignKey("student_solution.id", ondelete="CASCADE"),
        nullable=False,
        unique=True
    )

    teacher_id = db.Column(
        db.Integer,
        db.ForeignKey("teacher.id", ondelete="CASCADE"),
        nullable=False
    )

    # self columns
    score = db.Column(
        db.Integer,
        nullable=False
    )

    feedback = db.Column(db.String(ModelConstants.StringLength.MAX_FEEDBACK))

    # relationships
    solution = db.relationship(
        "StudentSolution",
        back_populates="grade"
    )

    teacher = db.relationship(
        "Teacher",
        back_populates="grades"
    )

    __table_args__ = (
        db.CheckConstraint(
            f"score >= {GeneralConstants.Score.MIN} AND score <= {GeneralConstants.Score.MAX}",
            name='valid_score_range'
        ),
    )