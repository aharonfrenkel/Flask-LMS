import re


def camelcase_to_snakecase(name: str) -> str:
    """
    Convert a CamelCase string to snake_case.

    Args:
        name: String in CamelCase format

    Returns:
        String in snake_case format
    Examples:
        >>> camelcase_to_snakecase('CamelCase')
        'camel_case'
        >>> camelcase_to_snakecase('HTTPResponse')
        'http_response'
    """
    return re.sub(r"(?<!^)(?=[A-Z])", "_", name)