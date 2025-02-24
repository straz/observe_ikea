from datetime import datetime
import os

# defined in Dockerfile
LOGFILE = os.getenv("LOGFILE")


def log(msg):
    now = datetime.now().isoformat()
    with open(LOGFILE, "a") as fp:
        fp.write(f"\n[{now}]: {msg}")
