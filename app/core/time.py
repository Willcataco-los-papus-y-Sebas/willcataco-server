from datetime import datetime
from zoneinfo import ZoneInfo

BOLIVIA = ZoneInfo("America/La_Paz")

class TimeBolivia:
    
    @staticmethod
    def format_date(date: datetime):
        to_bolivia = TimeBolivia.__get_time_zone(date)
        return to_bolivia.strftime("%d/%m/%Y")
    
    @staticmethod
    def format_datetime(date: datetime):
        to_bolivia = TimeBolivia.__get_time_zone(date)
        return to_bolivia.strftime("%d/%m/%Y  %H/%M")
    
    @staticmethod
    def __get_time_zone(time: datetime):
        if time.tzinfo is None:
            raise ValueError("Time no puede ser un naive") 
        if time.tzname() != 'UTC':
            raise ValueError("Time solo puede ser UTC")
        return time.astimezone(BOLIVIA)