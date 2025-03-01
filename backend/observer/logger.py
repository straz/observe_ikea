import logging
from datetime import datetime
from zoneinfo import ZoneInfo

from .config import LOCAL_TZ


class TimeZoneFormatter(logging.Formatter):
    def __init__(self, fmt=None, datefmt=None, timezone=LOCAL_TZ):
        format_str = "[%(asctime)s] %(levelname)s - %(message)s"
        super().__init__(fmt=format_str, datefmt=None)
        self.timezone = ZoneInfo(timezone)
        self.tz_name = self.timezone.tzname(datetime.now())  # string like 'EST'

    def formatTime(self, record: logging.LogRecord, datefmt=None) -> str:
        dt = datetime.fromtimestamp(record.created)
        local_dt = dt.replace().astimezone(self.timezone)
        return local_dt.strftime(f"%Y-%m-%d %H:%M {self.tz_name}")


LOG = logging.getLogger(__name__)
LOG.setLevel(logging.INFO)

handler = logging.StreamHandler()  # Or FileHandler('my_app.log')
handler.setFormatter(TimeZoneFormatter())
LOG.addHandler(handler)
