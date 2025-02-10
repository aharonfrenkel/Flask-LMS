from marshmallow import fields

from app.extensions import ma
from app.models import Teacher
from app.schemas import PersonSchema


class TeacherSchema(PersonSchema, ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Teacher
        load_instance = True
        exclude = ('date', 'time')

    courses = fields.Nested(
        'CourseSchema',
        many=True,
        dump_only=True,
        only=('name',)
    )

    lectures = fields.Nested(
        'LectureSchema',
        many=True,
        dump_only=True,
        only=('name', 'content')
    )

    courses_count = fields.Function(
        lambda obj: len(obj.courses),
        dump_only=True
    )

    lectures_count = fields.Function(
        lambda obj: len(obj.lectures),
        dump_only=True
    )