from app.extensions import db
from app.models import NameMixin


class Lecture(NameMixin):
    """
    Lecture model representing course content.

    Inherits from NameMixin which provides:
    - name field with validation

    Each lecture belongs to a course and can have multiple exercises.
    """

    course_id = db.Column(
        db.Integer,
        db.ForeignKey("course.id", ondelete="CASCADE"),
        nullable=False
    )

    teacher_id = db.Column(
        db.Integer,
        db.ForeignKey("teacher.id", ondelete="SET NULL")
    )

    content = db.Column(db.Text)

    course = db.relationship("Course", back_populates="lectures")
    teacher = db.relationship("Teacher", back_populates="lectures")
    exercises = db.relationship("Exercise", back_populates="lecture", cascade="all, delete-orphan")

    __table_args__ = (
        db.UniqueConstraint("name", "course_id", name="unique_lecture_name_per_course"),
    )