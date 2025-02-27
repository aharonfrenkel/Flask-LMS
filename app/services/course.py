from typing import List

from flask_login import current_user
from werkzeug.exceptions import Forbidden, Conflict, NotFound

from app.models import Course
from app.schemas import CourseWriteSchema
from app.services import CRUDService


class CourseService:
    def __init__(
            self,
            crud_service: CRUDService,
            course_write_schema: CourseWriteSchema
    ) -> None:
        self._crud_service = crud_service
        self._course_write_schema = course_write_schema


    # get courses service
    def get_accessible_courses(self) -> List[Course]:
        """
        Get courses based on user role.

        Returns:
            List of courses according to user's role and permissions:
            - Admin: All courses
            - Teacher: Courses they teach
            - Student: Courses they are enrolled in
        """
        if current_user.is_admin:
            return self._fetch_all_courses()
        if current_user.is_teacher:
            return self._fetch_teacher_courses()
        return self._fetch_student_courses()

    def _fetch_all_courses(self) -> List[Course]:
        return self._crud_service.find_all(Course)

    def _fetch_teacher_courses(self) -> List[Course]:
        return current_user.teacher.courses

    def _fetch_student_courses(self) -> List[Course]:
        return current_user.student.courses


    # create course service
    def create_course(self, data: dict) -> Course:
        """
        Create a new course.

        Args:
            data: Dict with 'name'

        Returns:
            The newly created course.

        Raises:
            Conflict: If course with same name already exists
        """
        self._verify_course_name_available(data['name'])
        return self._crud_service.create(data, self._course_write_schema)


    # get course service
    def get_course_by_name(self, course_name: str) -> Course:
        """
        Get course by name with appropriate access control.

        Args:
            course_name: The unique name of the course.

        Returns:
            Course object with appropriate level of detail

        Raises:
            NotFound: If course doesn't exist.
            Forbidden: If user doesn't have access to the course.
        """
        course = self._get_course_by_name_or_404(course_name)
        self._verify_course_access(course)
        return course

    def _verify_course_access(self, course: Course) -> None:
        if not self._has_course_access(course):
            raise Forbidden("You don't have access to this course")

    def _has_course_access(self, course: Course) -> bool:
        if current_user.is_admin:
            return True
        if current_user.is_teacher:
            return course in current_user.teacher.courses
        return course in current_user.student.courses


    # update course service
    def update_course(self, course_name: str, data: dict) -> Course:
        """
        Update a course's details.

        Args:
            course_name: Current name of the course
            data: Dict with fields to update (currently supports name field only)

        Returns:
            Updated Course object (updated or unchanged if no changes were needed)

        Raises:
            NotFound: If course doesn't exist
            Conflict: If trying to change name to one that already exists
        """
        course = self._get_course_by_name_or_404(course_name)
        if 'name' in data and course.name != data['name']:
            self._verify_course_name_available(data['name'])
            self._crud_service.update(course, **data)
        return course


    # delete course service
    def delete_course(self, course_name: str) -> None:
        """
        Delete a course.

        Args:
            course_name: The name of the course

        Raises:
            NotFound: If course doesn't exist

        Notes:
            This operation will also cascade delete all related records
            including lectures, exercises, and enrollment relationships
            for teachers and students.
        """
        course = self._get_course_by_name_or_404(course_name)
        self._crud_service.delete(course)


    def _get_course_by_name_or_404(self, course_name: str) -> Course:
        return self._crud_service.find_one_by_fields_or_raise(
            model=Course,
            name=course_name,
            exception=NotFound,
            error_msg=f"Course '{course_name}' not found"
        )

    def _verify_course_name_available(self, course_name: str) -> None:
        self._crud_service.validate_no_record_by_fields(
            model=Course,
            exception=Conflict,
            error_msg=f"Course with name '{course_name}' already exists",
            name=course_name
        )