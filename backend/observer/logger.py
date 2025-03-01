from datetime import datetime, timezone
from zoneinfo import ZoneInfo

from .config import LOCAL_TZ, LOGFILE


def console_log(msg):
    now_utc = datetime.now(timezone.utc)
    now_local = now_utc.astimezone(ZoneInfo(LOCAL_TZ))
    tz = now_local.tzname()
    tstamp = now_local.strftime(f"%Y-%m-%dT%H:%M {tz}")
    with open(LOGFILE, "a") as fp:
        message = f"\n[{tstamp}]: {msg}"
        fp.write(message)
        print(message)
