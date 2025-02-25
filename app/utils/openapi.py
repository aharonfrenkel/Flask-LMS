from dataclasses import dataclass
from http import HTTPStatus

from marshmallow import Schema


__all__ = [
    'ParameterConfig',
    'ParametersConfig',
    'RequestBodyConfig',
    'ResponseConfig',
    'ResponsesConfig',
    'create_endpoint_doc'
]


@dataclass
class ParameterConfig:
    name: str
    description: str
    location: str = 'path'
    required: bool = True
    schema_type: str = 'string'


@dataclass
class ParametersConfig:
    parameters: list[ParameterConfig]
    description: str = None


@dataclass
class RequestBodyConfig:
    schema: Schema
    description: str = None
    required: bool = True
    content_type: str = 'application/json'


@dataclass
class ResponseConfig:
    code: HTTPStatus | str | int
    description: str
    content_type: str = 'application/json'
    schema: Schema = None


@dataclass
class ResponsesConfig:
    responses: list[ResponseConfig]
    description: str = None

def create_endpoint_doc(
        tags: list[str],
        summary: str,
        description: str,
        security: list[dict[str, list]] = None,
        parameters: ParametersConfig = None,
        request_body: RequestBodyConfig = None,
        responses: ResponsesConfig = None
) -> dict:
    """
    Create standardized OpenAPI documentation for an API endpoint.

    This function generates a complete OpenAPI specification object for a single
    endpoint, including metadata, parameters, request format, and response structures.
    It ensures consistent documentation across all API endpoints.

    Args:
        tags: List of category tags to organize endpoints (e.g., ['Authentication'])
        summary: Short one-line summary of what the endpoint does
        description: Detailed multi-line description of endpoint functionality
        security: List of security requirements (e.g., [{'cookieAuth': []}])
        parameters: Configuration for URL path and query parameters
        request_body: Configuration for the request payload
        responses: Configuration for all possible response types

    Returns:
        dict: Complete OpenAPI specification object for the endpoint
    """
    doc = {
        'tags': tags,
        'summary': summary,
        'description': description
    }

    if security:
        doc['security'] = security

    if parameters:
        doc['parameters'] = _create_parameters(parameters)

    if request_body:
        doc['requestBody'] = _create_request_body(request_body)

    if responses:
        doc['responses'] = _create_responses(responses)

    return doc


def _create_parameters(parameters: ParametersConfig) -> list:
    params_list = [
        {
            'in': parameter.location,
            'name': parameter.name,
            'required': parameter.required,
            'description': parameter.description,
            'schema': {
                'type': parameter.schema_type
            }
        }
        for parameter in parameters.parameters
    ]

    if parameters.description:
        params_list.append({
            'description': parameters.description
        })

    return params_list


def _create_request_body(request_body: RequestBodyConfig) -> dict:
    body_doc = {
        'required': request_body.required,
        'content': {
            request_body.content_type: {
                'schema': request_body.schema
            }
        }
    }

    if request_body.description:
        body_doc['description'] = request_body.description

    return body_doc


def _create_responses(responses: ResponsesConfig) -> dict:
    body_doc = {}

    if responses.description:
        body_doc['description'] = responses.description

    for response in responses.responses:
        body_doc[response.code] = {
            'description': response.description
        }
        if response.schema:
            body_doc[response.code]['content'] = {
                response.content_type: {
                    'schema': response.schema
                }
            }

    return body_doc