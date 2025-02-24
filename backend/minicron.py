# This script runs forever, pinging "http://localhost:/trigger" every minute

# /// script
# requires-python = ">=3.12"
# dependencies = ['requests']
# ///

from datetime import datetime
from typing import Callable
import time
import requests
from observer.logger import log


def send_trigger():
    url = "http://localhost:8000/trigger"
    try:
        requests.get(url)
    except requests.exceptions.ConnectionError as err:
        log(f"trigger failed: {err}")


def every_minute(fcn: Callable):
    while True:
        now = datetime.now()
        log("Observation triggered")
        fcn()
        sleep_time = 60 - now.second
        time.sleep(sleep_time)


def main():
    # before the first request, give the web server a sec to start up
    time.sleep(1)
    every_minute(send_trigger)


if __name__ == "__main__":
    main()
