from http import HTTPStatus

from flask import Blueprint, Response
from flask_login import login_required

from app.constants import AuthConstants
from app.factories import lecture_schema, lecture_service
from app.middleware import handle_exceptions, role_required, validate_json_request
from app.utils import success_response


lecture_bp = Blueprint('lecture', __name__, url_prefix='/course/<string:course_name>/lecture')


@lecture_bp.post('/')
@handle_exceptions
@login_required
@role_required(AuthConstants.Role.ADMIN, AuthConstants.Role.TEACHER)
@validate_json_request(lecture_schema)
def create_lecture(course_name: str, data: dict) -> Response:
    lecture = lecture_service.create_lecture(course_name, data)

    return success_response(
        f"Lecture '{lecture.name}' created successfully",
        data=lecture,
        schema=lecture_schema,
        status_code=HTTPStatus.CREATED
    )


@lecture_bp.put('/<string:lecture_name>')
@handle_exceptions
@login_required
@role_required(AuthConstants.Role.ADMIN, AuthConstants.Role.TEACHER)
@validate_json_request(lecture_schema, partial=True)
def update_lecture(course_name: str, lecture_name: str, data: dict) -> Response:
    lecture = lecture_service.update_lecture(course_name, lecture_name, data)

    return success_response(
        "Lecture updated successfully",
        data=lecture,
        schema=lecture_schema
    )


@lecture_bp.delete('/<string:lecture_name>')
@handle_exceptions
@login_required
@role_required(AuthConstants.Role.ADMIN, AuthConstants.Role.TEACHER)
def delete_lecture(course_name: str, lecture_name: str) -> Response:
    lecture_service.delete_lecture(course_name, lecture_name)

    return success_response(
        status_code=HTTPStatus.NO_CONTENT
    )