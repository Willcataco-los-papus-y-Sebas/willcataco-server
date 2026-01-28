from datetime import datetime
from zoneinfo import ZoneInfo

BOLIVIA = ZoneInfo("America/La_Paz")

class TimeBolivia:
    @staticmethod
    def get_time_zone(time: datetime, format: str):
        if time.tzinfo is None:
            raise ValueError("Time no puede ser un naive") 
        if time.tzname() != 'UTC':
            raise ValueError("Time solo puede ser UTC")
        return time.astimezone(BOLIVIA).strftime(format)