from app.extensions import db


class StudentCourses(db.Model):
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


class TeacherCourses(db.Model):
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