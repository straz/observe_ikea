import logging
from datetime import datetime
from zoneinfo import ZoneInfo

from .config import LOCAL_TZ


class TimeZoneFormatter(logging.Formatter):
    def __init__(self, fmt=None, datefmt=None, timezone=LOCAL_TZ):
        super().__init__(fmt, datefmt)
        self.timezone = ZoneInfo(timezone)
        self.tz_name = self.timezone.tzname(datetime.now())  # string like 'EST'

    def converter(self, timestamp):
        dt = datetime.datetime.fromtimestamp(timestamp)
        return dt.replace().astimezone(self.timezone)

    def format(self, record: logging.LogRecord):
        date_str = f"%Y-%m-%d %H:%M {self.tz_name}"
        format_str = "[%(asctime)s] %(levelname)s - %(message)s"
        formatter = logging.Formatter(fmt=format_str, datefmt=date_str)
        return formatter.format(record)


LOG = logging.getLogger(__name__)
LOG.setLevel(logging.INFO)

handler = logging.StreamHandler()  # Or FileHandler('my_app.log')
handler.setFormatter(TimeZoneFormatter())
LOG.addHandler(handler)
