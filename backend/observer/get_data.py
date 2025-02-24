from datetime import datetime, timezone
import requests

from .ikea import get_devices, filter_attributes, NOT_IMPLEMENTED
from .database import Database
from .logger import log


def log_device(db: Database, now: datetime, device: dict):
    event = device["deviceType"]
    device_id = device["id"]
    if event in NOT_IMPLEMENTED:
        return
    data = filter_attributes(event, device["attributes"])
    db.write_log_dedupe(timestamp=now, event=event, device=device_id, data=data)


def log_event(db: Database, now: datetime, event: str, device: str, data: dict):
    db.write_log_dedupe(timestamp=now, event=event, device=device, data=data)


def log_all_devices():
    now = datetime.now(timezone.utc)
    db = Database(month=now.month, year=now.year)
    try:
        for device in get_devices():
            log_device(db=db, now=now, device=device)
    except requests.exceptions.ConnectionError as err:
        log(f"Dirigera connection error: {err}")
        log_event(
            db=db,
            event="dirigera_connection_error",
            device="",
            data={"error": str(err)},
        )
    except requests.exceptions.ConnectTimeout as err:
        log(f"Dirigera timeout: {err}")
        log_event(
            db=db,
            now=now,
            event="dirigera_timeout",
            device="",
            data={"error": str(err)},
        )
