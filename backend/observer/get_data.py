"""
Get data from the sensors connected to the IKEA DIRIGERA zigbee hub.
Log the data into the local database.
"""

from datetime import datetime, timedelta

from .ikea import filter_attributes, NOT_IMPLEMENTED
from .database import Database
from .logger import log
from .send_mail import send_mail


def log_device(db: Database, now: datetime, device: dict):
    event = device["deviceType"]
    device_id = device["id"]
    if event in NOT_IMPLEMENTED:
        return
    data = filter_attributes(event, device["attributes"])
    if event == "motionSensor" and data["attributes"]["isDetected"] is True:
        notify_if_new(db=db, now=now)

    log_event(db=db, now=now, event=event, device_id=device_id, data=data)


def notify_if_new(db: Database, now: datetime):
    """
    If we see motion (isDetected=True), and nothing has happened in the
    last hour, then send an email.
    """
    query = "select * from log where event = 'motionSensor' and timestamp > ?;"
    past = now - timedelta(hours=1)
    rows = db.execute_fetchall(query, (past,))
    if len(rows) == 0:
        send_mail("something's up", "IKEA observer")


def log_event(db: Database, now: datetime, event: str, device_id: str, data: dict):
    db.write_log_dedupe(timestamp=now, event=event, device=device_id, data=data)


def log_error(db: Database, now: datetime, event: str, err: Exception):
    log(f"{event}: {err}")
    log_event(
        db=db,
        now=now,
        event=event,
        device_id="",
        data={"error": str(err)},
    )
