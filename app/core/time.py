from datetime import datetime, date, timezone, time, timedelta
from zoneinfo import ZoneInfo

BOLIVIA = ZoneInfo("America/La_Paz")

class TimeBolivia:
    
    @staticmethod
    def format_date(date: datetime):
        to_bolivia = TimeBolivia.__get_time_zone_datetime(date)
        return to_bolivia.strftime("%d/%m/%Y")
    
    @staticmethod
    def format_datetime(date: datetime):
        to_bolivia = TimeBolivia.__get_time_zone_datetime(date)
        return to_bolivia.strftime("%d/%m/%Y %H:%M")
    
    @staticmethod
    def format_correct(date: date):
        to_datetime = datetime.combine(date, time.min)
        to_UTC = to_datetime.astimezone(timezone.utc)
        correct_time = to_UTC + timedelta(hours=4)
        return correct_time
    
    @staticmethod
    def __get_time_zone_datetime(time: datetime):
        if time.tzinfo is None:
            time = time.replace(tzinfo = timezone.utc) 
        if time.tzname() != 'UTC':
            raise ValueError("Parameter 'time' only can be in format UTC")
        return time.astimezone(BOLIVIA)