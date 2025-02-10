from datetime import datetime

import pytz
from marshmallow import fields, validate

from app.extensions import ma
from app.models import Exercise
from app.schemas import NameSchema


class ExerciseSchema(NameSchema, ma.SQLAlchemyAutoSchema):
    """
    Schema for Exercise model with deadline handling and solution protection.

    Manages exercise content, submission deadlines, and controlled access to teacher solutions.
    """

    class Meta:
        model = Exercise
        load_instance = True
        exclude = ('time',)

    content = fields.Str(
        required=True,
        validate=[
            validate.Length(
                min=1,
                error="content cannot be empty"
            )
        ]
    )

    target_date = fields.DateTime(
        min=datetime.now(),
        error="Target date must be in the future"
    )

    is_mandatory = fields.Boolean()

    teacher_solution = fields.Method(
        'get_teacher_solution',
        validate_str=True,
        validate=[
            validate.Length(
                min=1,
                error="teacher_solution cannot be empty"
            )
        ]
    )

    def get_teacher_solution(self, obj):
        current_time = datetime.now(pytz.utc)
        if current_time >= obj.target_date:
            return obj.teacher_solution