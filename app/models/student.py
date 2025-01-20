from app.extensions import db
from app.models.mixins import PersonMixin


class Student(PersonMixin):
    """
    Student model with relationships to courses and exercise solutions.

    Inherits from PersonMixin which provides:
    - user_id (link to User model)
    - first_name
    - last_name
    - phone
    - email
    """

    courses = db.relationship(
        "Course",
        secondary="student_courses",
        back_populates="students"
    )

    solutions = db.relationship(
        "StudentSolution",
        back_populates="student",
        cascade="all, delete-orphan"
    )