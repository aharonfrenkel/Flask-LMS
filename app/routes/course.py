from http import HTTPStatus

from flask import Blueprint, Response
from flask_login import login_required, current_user

from app.constants import AuthConstants
from app.factories import (
    course_service,
    course_write_schema,
    course_read_schema,
    course_read_list_schema,
    course_admin_schema,
    course_admin_list_schema
)
from app.middleware import handle_exceptions, validate_json_request, role_required
from app.utils import success_response


course_bp = Blueprint('course', __name__, url_prefix='/course')


@course_bp.get('/')
@handle_exceptions
@login_required
def get_courses() -> Response:
    courses = course_service.get_accessible_courses()

    return success_response(
        message="Courses retrieved successfully",
        data=courses,
        schema=course_read_list_schema if current_user.is_student else course_admin_list_schema
    )


@course_bp.post('/')
@handle_exceptions
@login_required
@role_required(AuthConstants.Role.ADMIN)
@validate_json_request(course_write_schema)
def create_course(data: dict) -> Response:
    course = course_service.create_course(data)

    return success_response(
        f"Course '{course.name}' created successfully",
        data=course,
        schema=course_write_schema,
        status_code=HTTPStatus.CREATED
    )


@course_bp.get('/<string:course_name>')
@handle_exceptions
@login_required
def get_course(course_name: str) -> Response:
    course = course_service.get_course_by_name(course_name)

    return success_response(
        "Course details retrieved successfully",
        data=course,
        schema=course_read_schema if current_user.is_student else course_admin_schema
    )


@course_bp.put('/<string:course_name>')
@handle_exceptions
@login_required
@role_required(AuthConstants.Role.ADMIN)
@validate_json_request(course_write_schema, partial=True)
def update_course(course_name: str, data: dict) -> Response:
    course = course_service.update_course(course_name, data)

    return success_response(
        f"Course updated successfully",
        data=course,
        schema=course_admin_schema
    )


@course_bp.delete('/<string:course_name>')
@handle_exceptions
@login_required
@role_required(AuthConstants.Role.ADMIN)
def delete_course(course_name: str) -> Response:
    course_service.delete_course(course_name)

    return success_response(
        status_code=HTTPStatus.NO_CONTENT
    )