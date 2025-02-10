from marshmallow import fields

from app.extensions import ma
from app.models import Course
from app.schemas import NameSchema


class CourseSchema(NameSchema, ma.SQLAlchemyAutoSchema):
    """
    Schema for Course model with nested relationships and computed fields.

    Supports serialization of related lectures, teachers, and students,
    along with count calculations for each relationship.
    """

    class Meta:
        model = Course
        load_instance = True
        exclude = ('date', 'time')

    lectures = fields.Nested(
        'LectureSchema',
        many=True,
        dump_only=True
    )

    teachers = fields.Nested(
        'TeacherSchema',
        many=True,
        dump_only=True,
        only=('first_name', 'last_name')
    )

    students = fields.Nested(
        'StudentSchema',
        many=True,
        dump_only=True,
        only=('first_name', 'last_name')
    )

    # Computed fields for relationship counts
    lectures_count = fields.Function(
        lambda obj: len(obj.lectures),
        dump_only=True
    )

    teachers_count = fields.Function(
        lambda obj: len(obj.teachers),
        dump_only=True
    )

    students_count = fields.Function(
        lambda obj: len(obj.students),
        dump_only=True
    )