import json
from datetime import datetime
from .database import Database


def query_devices(year: int, month: int):
    db = Database(year=year, month=month)
    return [row[0] for row in db.query_devices()]


def query_day(device_id: str, year: int, month: int, day: int):
    db = Database(year=year, month=month)
    rows = db.query_day(device_id=device_id, day=day)
    return [decode_row(r) for r in rows]


def decode_row(row):
    timestamp, data = row
    return {"timestamp": datetime.fromisoformat(timestamp)} | json.loads(data)
