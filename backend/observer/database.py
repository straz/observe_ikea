import json
import sqlite3
from contextlib import closing
from datetime import datetime

from .path import DATADIR
from .logger import LOG


def adapt_datetime_iso(val):
    """Adapt datetime.datetime to timezone-naive ISO 8601 date."""
    return val.isoformat()


def convert_datetime(val):
    """Convert ISO 8601 datetime to datetime.datetime object."""
    return datetime.fromisoformat(val.decode())


sqlite3.register_adapter(datetime, adapt_datetime_iso)
sqlite3.register_converter("datetime", convert_datetime)


CREATE = """CREATE TABLE IF NOT EXISTS log(
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      timestamp TEXT,
      event TEXT,
      device TEXT,
      data TEXT)"""

CREATE_INDEX = "CREATE INDEX timestamp_idx on log(timestamp)"


class Database:
    """
    Sharded by month
    """

    def __init__(self, month: int, year: int):
        self.month = month
        self.year = year
        self.init_conn()

    def init_conn(self) -> sqlite3.Connection:
        file = DATADIR / f"data-{self.year}-{self.month:02}.db"
        self.conn = sqlite3.connect(file)
        self.execute(CREATE)
        try:
            self.execute(CREATE_INDEX)
        except sqlite3.OperationalError:
            # index already exists
            pass
        self.conn.commit()
        return self.conn

    def execute(self, query, *args):
        with closing(self.conn.cursor()) as cursor:
            return cursor.execute(query, *args)

    def execute_fetchone(self, query, *args):
        with closing(self.conn.cursor()) as cursor:
            cursor.execute(query, *args)
            return cursor.fetchone()

    def execute_fetchall(self, query, *args):
        with closing(self.conn.cursor()) as cursor:
            cursor.execute(query, *args)
            return cursor.fetchall()

    def write_log_dedupe(
        self, timestamp: datetime, event: str, device: str, data: dict
    ):
        last_query = "SELECT data FROM log WHERE device = ? ORDER BY id DESC LIMIT 1"
        last_entry = self.execute_fetchone(last_query, (device,))
        if last_entry and last_entry[0] == json.dumps(data):
            LOG.info(f"skipping: {event} {data}")
            return
        insert = "INSERT INTO log(timestamp, event, device, data) VALUES(?, ?, ?, ?);"
        self.execute(insert, (timestamp, event, device, json.dumps(data)))
        self.conn.commit()

    def write_log(self, timestamp: datetime, event: str, device: str, data: dict):
        insert = "INSERT INTO log(timestamp, event, device, data) VALUES(?, ?, ?, ?);"
        self.execute(insert, (timestamp, event, device, json.dumps(data)))
        self.conn.commit()

    def query_devices(self):
        query = "SELECT DISTINCT device FROM log;"
        return self.execute_fetchall(query)

    def query_day(self, device_id: str, day: int):
        read_day = """
          SELECT timestamp, data FROM log
            WHERE device = ?
            AND CAST(strftime('%d', timestamp) AS INTEGER)  = ?
            ORDER BY id ASC;
        """
        return self.execute_fetchall(read_day, (device_id, day))
