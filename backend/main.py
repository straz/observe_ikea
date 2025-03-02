# This script runs a web server that reads+writes device observation data

from pathlib import Path
import os

from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

from observer import Home, query_day, query_devices

LOGFILE = os.getenv("LOGFILE")


app = FastAPI()

# Create Home instances from config.py
Home.init_all()


@app.get("/")
async def root() -> dict:
    return {"message": "Hello, World!"}


@app.get("/trigger")
async def trigger_observation() -> dict:
    """
    We receive a trigger once every minute.
    This runs log_all_devices on each Home,
    which will observe the data and record it.
    """
    Home.log_all()
    return {"message": "Observation triggered."}


@app.get("/log", response_class=PlainTextResponse)
async def show_log() -> str:
    """
    Returns the low-level logs, mostly good for debugging.
    """
    log = Path(LOGFILE)
    text = log.read_text()
    return text or "logfile is empty"


"""
GET /data/{device_id}/day/{year}/{month}/{day}
GET /data/{device_id}/week/{year}/{month}/{start_day}
GET /data/{device_id}/month/{year}/{month}

"""


@app.get("/devices/{year}/{month}")
async def list_devices(year: int, month: int):
    return query_devices(year=year, month=month)


@app.get("/sensors")
async def all_sensors():
    return Home.all_current_sensors()


@app.get("/data/{device_id}/day/{year}/{month}/{day}")
async def get_day_data(device_id: str, year: int, month: int, day: int):
    return query_day(device_id=device_id, year=year, month=month, day=day)
