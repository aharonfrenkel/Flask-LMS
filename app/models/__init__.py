from .base_table import BaseTable
from .mixins import NameMixin, PersonMixin

from .user import User
from .login_record import LoginRecord
from .token import Token

from .associations import StudentCourses, TeacherCourses

from .student import Student
from .teacher import Teacher
from .course import Course
from .lecture import Lecture
from .exercise import Exercise
from .student_solution import StudentSolution
from .grade import Grade