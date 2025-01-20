from app.extensions import db
from app.models import NameMixin


class Course(NameMixin):
    """
    Course model representing an academic course.

    Inherits from NameMixin which provides:
    - name field with validation

    Additional fields track course details, status, and dates.
    Relationships connect to students, teachers, and content.
    """

    lectures = db.relationship(
        "Lecture",
        back_populates="course",
        cascade="all, delete-orphan"
    )

    teachers = db.relationship(
        "Teacher",
        secondary="teacher_courses",
        back_populates="courses"
    )

    students = db.relationship(
        "Student",
        secondary="student_courses",
        back_populates="courses"
    )

    __table_args__ = (
        db.UniqueConstraint("name", name="unique_course"),
    )