from app.extensions import db
from app.models.mixins import PersonMixin


class Teacher(PersonMixin):
    """
    Teacher model with relationships to courses, lectures, and grades.

    Inherits from PersonMixin which provides:
    - user_id (link to User model)
    - first_name
    - last_name
    - phone
    - email
    """

    courses = db.relationship(
        "Course",
        secondary="teacher_courses",
        back_populates="teachers"
    )
    lectures = db.relationship("Lecture", back_populates="teacher")
    exercises = db.relationship("Exercise", back_populates="teacher")
    grades = db.relationship("Grade", back_populates="teacher")