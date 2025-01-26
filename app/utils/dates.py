

def format_date(datetime_obj) -> str:
    return datetime_obj.strftime("%d-%m-%Y")

def format_time(datetime_obj) -> str:
    return datetime_obj.strftime("%H:%M:%S")