from marshmallow import fields

from app.extensions import ma
from app.models import Student
from app.schemas import PersonSchema


class StudentSchema(PersonSchema, ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Student
        load_instance = True
        exclude = ('date', 'time')

    courses = fields.Nested(
        'CourseSchema',
        many=True,
        dump_only=True,
        only=('name',)
    )

    solutions = fields.Nested(
        'StudentSolutionSchema',
        many=True,
        dump_only=True
    )

    courses_count = fields.Function(
        lambda obj: len(obj.courses),
        dump_only=True
    )