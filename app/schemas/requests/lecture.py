from marshmallow import fields, validate

from app.extensions import ma
from app.models import Lecture
from app.schemas import NameSchema


class LectureSchema(NameSchema, ma.SQLAlchemyAutoSchema):
    """
    Schema for Lecture model with content validation and relationships.

    Includes content validation, teacher information, and exercise tracking.
    """

    class Meta:
        model = Lecture
        load_instance = True
        exclude = ('time',)

    content = fields.Str(
        validate=[
            validate.Length(
                min=1,
                error="content cannot be empty"
            )
        ]
    )

    teacher = fields.Nested(
        'TeacherSchema',
        dump_only=True,
        only=('first_name', 'last_name')
    )

    exercises = fields.Nested(
        'ExerciseSchema',
        many=True,
        dump_only=True
    )

    exercises_count = fields.Function(
        lambda obj: len(obj.exercises),
        dump_only=True
    )