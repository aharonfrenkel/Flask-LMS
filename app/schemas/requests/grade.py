from marshmallow import fields, validate

from app.extensions import ma
from app.constants import GeneralConstants, ValidationConstants, ModelConstants
from app.models import Grade


class GradeSchema(ma.SQLAlchemyAutoSchema):
    """
    Schema for Grade model.

    Supports grade submission and retrieval with validations.

    Relationships include teacher details while protecting internal IDs.
    Enforces score range and feedback length constraints.
    """

    class Meta:
        model = Grade
        load_instance = True
        exclude = ('date', 'time')

    teacher_id = fields.Int(
        required=True,
        load_only=True
    )

    solution_id = fields.Int(
        required=True,
        load_only=True
    )

    score = fields.Int(
        required=True,
        validate=[
            validate.Range(
                min=GeneralConstants.Score.MIN,
                max=GeneralConstants.Score.MAX,
                error=ValidationConstants.Score.ERROR_MESSAGES['range']
            )
        ]
    )

    feedback = fields.Str(
        validate=[
            validate.Length(
                min=1,
                max=ModelConstants.StringLength.MAX_FEEDBACK,
                error=ValidationConstants.Feedback.ERROR_MESSAGES['length']
            )
        ]
    )

    teacher = fields.Nested(
        'TeacherSchema',
        only=('first_name', 'last_name'),
        dump_only=True
    )