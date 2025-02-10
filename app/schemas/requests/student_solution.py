from marshmallow import fields, validate

from app.extensions import ma
from app.constants import GeneralConstants
from app.models import StudentSolution


class StudentSolutionSchema(ma.SQLAlchemyAutoSchema):
    """
    Schema for StudentSolution model.

    Manages exercise solution submission and retrieval.
    Includes submission timestamp, status tracking, and grade information.

    Relationships track student, exercise and grade details while
    protecting internal IDs.
    """

    class Meta:
        model= StudentSolution
        load_instance = True
        exclude = ('date', 'time')

    student_id = fields.Int(
        required=True,
        load_only=True
    )

    exercise_id = fields.Int(
        required=True,
        load_only=True
    )

    content = fields.Str(
        required=True,
        validate=[
            validate.Length(
                min=1,
                error="content cannot be empty"
            )
        ]
    )

    submitted_at = fields.DateTime(
        dump_only=True,
        format="%d-%m-%Y %H:%M:%S"
    )

    status = fields.Str(
        validate=validate.OneOf(
            GeneralConstants.Status.CHOICES,
            error="Invalid status"
        )
    )

    student = fields.Nested(
        'StudentSchema',
        dump_only=True,
        only=('first_name', 'last_name')
    )

    exercise = fields.Nested(
        'ExerciseSchema',
        dump_only=True
    )

    grade = fields.Nested(
        'GradeSchema',
        dump_only=True,
        only=('score', 'feedback')
    )