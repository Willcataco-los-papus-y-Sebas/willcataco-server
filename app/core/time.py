from datetime import datetime
from zoneinfo import ZoneInfo

BOLIVIA = ZoneInfo("America/La_Paz")

def get_time_zone(time: datetime):
    return time.astimezone(BOLIVIA)