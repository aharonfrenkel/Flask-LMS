from .base import BaseSchema, NameSchema, PersonSchema

from .auth import (
    UserRegisterSchema,
    UserLoginSchema,
    UserForgetPasswordSchema,
    UserResetPasswordSchema,
    UserChangePasswordSchema,
    UserAdminSchema
)
from .course import CourseSchema
from .exercise import ExerciseSchema
from .grade import GradeSchema
from .lecture import LectureSchema
from .login_record import LoginRecordSchema
from .student import StudentSchema
from .student_solution import StudentSolutionSchema
from .teacher import TeacherSchema