from marshmallow import fields

from app.extensions import ma
from app.models import Course
from app.schemas import NameSchema


__all__ = [
    'CourseWriteSchema',
    'CourseReadSchema',
    'CourseAdminSchema'
]


class BaseCourseSchema(NameSchema, ma.SQLAlchemyAutoSchema):
    """
    Schema for Course model with nested relationships and computed fields.

    Supports serialization of related lectures, teachers, and students,
    along with count calculations for each relationship.
    """

    class Meta:
        model = Course
        load_instance = True
        exclude = ('id', 'created_at', 'date', 'time')


class CourseWriteSchema(BaseCourseSchema):
    """
    Schema for course creation and update operations.

    Used to validate input data when creating or modifying courses.
    For partial updates, use with `partial=True` parameter.
    """
    pass


class CourseReadSchema(BaseCourseSchema):
    """
    Schema for course data retrieval with related lectures and teachers.

    Includes nested relationships and computed counts for general course views.
    All relationship fields are read-only.
    """
    lectures = fields.Nested(
        'LectureSchema',
        many=True,
        dump_only=True
    )

    teachers = fields.Nested(
        'TeacherSchema',
        many=True,
        dump_only=True,
        only=('full_name',)
    )

    lectures_count = fields.Function(
        lambda obj: len(obj.lectures),
        dump_only=True
    )

    teachers_count = fields.Function(
        lambda obj: len(obj.teachers),
        dump_only=True
    )


class CourseAdminSchema(CourseReadSchema):
    """
    Extended course schema with student information for administrators.

    Adds student data to the standard course view for privileged users.
    Includes list of enrolled students and their count.
    """
    students = fields.Nested(
        'StudentSchema',
        many=True,
        dump_only=True,
        only=('full_name',)
    )

    students_count = fields.Function(
        lambda obj: len(obj.students),
        dump_only=True
    )