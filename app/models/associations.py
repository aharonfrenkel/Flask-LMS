"""
This module defines the many-to-many association tables for the application.
These tables manage the relationships between:
- Students and their courses
- Teachers and their courses
"""

from app.extensions import db
from app.models import BaseTable


class StudentCourses(BaseTable):
    """Association table connecting students with their courses."""

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("student.id", ondelete="CASCADE"),
        primary_key=True
    )

    course_id = db.Column(
        db.Integer,
        db.ForeignKey("course.id", ondelete="CASCADE"),
        primary_key=True
    )


class TeacherCourses(BaseTable):
    """Association table connecting teachers with their courses."""

    teacher_id = db.Column(
        db.Integer,
        db.ForeignKey("teacher.id", ondelete="CASCADE"),
        primary_key=True
    )

    course_id = db.Column(
        db.Integer,
        db.ForeignKey("course.id", ondelete="CASCADE"),
        primary_key=True
    )