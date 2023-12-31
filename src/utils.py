from datetime import datetime, timezone

from src.config import DATE_TIME_FORMAT


def date_time_to_str_gmt(value: datetime) -> str:
    try:
        if not value.tzinfo:
            value = value.replace(tzinfo=timezone.utc)
        return value.strftime(DATE_TIME_FORMAT)
    except:
        return ""


def str_to_date_time_gmt(value) -> datetime:
    try:
        parsed_date = datetime.strptime(value, DATE_TIME_FORMAT)
        parsed_date = parsed_date.replace(microsecond=0)
        return parsed_date
    except ValueError as e:
        raise ValueError(f"Invalid datetime format. Expected format: {DATE_TIME_FORMAT}. Error: {e}")
