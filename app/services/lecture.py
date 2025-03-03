from flask_login import current_user
from werkzeug.exceptions import Conflict, NotFound

from app.models import Course
from app.schemas import LectureSchema
from app.services import CRUDService, CourseService


class LectureService:
    def __init__(
            self,
            crud_service: CRUDService,
            course_service: CourseService,
            lecture_schema: LectureSchema
    ) -> None:
        self._crud_service = crud_service
        self._course_service = course_service
        self._lecture_schema = lecture_schema


    # Create lecture service
    def create_lecture(self, course_name: str, data: dict):
        """
        Create a new lecture for a course.

        Args:
            course_name: The name of the course to add the lecture to
            data: Dict with lecture details (name, content, etc.)

        Returns:
            The newly created lecture

        Raises:
            NotFound: If course doesn't exist
            Forbidden: If user (teacher) doesn't have access to the course
            Conflict: If lecture with the same name already exists
        """
        course = self._course_service.get_course_by_name(course_name)
        self._verify_lecture_name_available(course, data['name'])
        lecture_data = self._prepare_lecture_data(data, course)
        return self._crud_service.create(lecture_data, self._lecture_schema)

    def _prepare_lecture_data(self, data: dict, course: Course) -> dict:
        lecture_data = data.copy()
        lecture_data['course_id'] = course.id
        if current_user.is_teacher:
            lecture_data['teacher_id'] = current_user.teacher.id
        return lecture_data


    # Update lecture service
    def update_lecture(self, course_name: str, lecture_name: str, data: dict):
        """
        Update an existing lecture.

        Args:
            course_name: The name of the course the lecture belongs to
            lecture_name: Current name of the lecture to update
            data: Dict with fields to update

        Returns:
            Updated lecture object

        Raises:
            NotFound: If course or lecture doesn't exist
            Forbidden: If user (teacher) doesn't have access to the course
            Conflict: If trying to rename to a name that already exists
        """
        course = self._course_service.get_course_by_name(course_name)
        lecture = self._get_lecture_by_name_or_404(course, lecture_name)
        if 'name' in data and lecture.name != data['name']:
            self._verify_lecture_name_available(course, data['name'])
        self._crud_service.update(lecture, **data)
        return lecture


    # Delete lecture service
    def delete_lecture(self, course_name: str, lecture_name: str) -> None:
        """
        Delete a lecture from a course.

        Args:
            course_name: The name of the course the lecture belongs to
            lecture_name: The name of the lecture to delete

        Raises:
            NotFound: If course or lecture doesn't exist
            Forbidden: If user (teacher) doesn't have access to the course
        """
        course = self._course_service.get_course_by_name(course_name)
        lecture = self._get_lecture_by_name_or_404(course, lecture_name)
        self._crud_service.delete(lecture)


    def _get_lecture_by_name(self, course: Course, lecture_name: str):
        return next(
            (lecture for lecture in course.lectures if lecture.name == lecture_name),
            None
        )

    def _get_lecture_by_name_or_404(self, course: Course, lecture_name: str):
        lecture = self._get_lecture_by_name(course, lecture_name)
        if not lecture:
            raise NotFound(f"Lecture with name '{lecture_name}' not found in this course")
        return lecture

    def _verify_lecture_name_available(self, course: Course, lecture_name: str) -> None:
        existing_lecture = self._get_lecture_by_name(course, lecture_name)
        if existing_lecture:
            raise Conflict(f"Lecture with name '{lecture_name}' already exists in this course")