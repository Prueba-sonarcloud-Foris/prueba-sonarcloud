from datetime import datetime

from result import Result, Ok, Err


def validate_time(time_input: str) -> Result:
    try:
        return Ok(datetime.strptime(time_input, '%H:%M').time())
    except ValueError:
        return Err('Invalid date')
