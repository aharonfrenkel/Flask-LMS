from datetime import date, datetime, time
from typing import Union


__all__ = [
    'format_date',
    'format_time'
]


def format_date(dt_obj: Union[date, datetime]) -> str:
    """
    Format a datetime object to a date string.

    Args:
        dt_obj: datetime object to be formatted

    Returns:
        String in dd/mm/yyyy format

    Examples:
        >>> format_date(datetime(2020, 5, 13, 17, 53, 26))
        '13/05/2020'
    """
    return f'{dt_obj:%d/%m/%Y}'

def format_time(dt_obj: Union[datetime, time]) -> str:
    """
    Format a datetime object to a time string.

    Args:
        dt_obj: datetime object to be formatted

    Returns:
        String in HH:MM:SS format

    Examples:
        >>> format_time(datetime(2020, 5, 13, 17, 53, 26))
        '17:53:26'
    """
    return f'{dt_obj:%H:%M:%S}'