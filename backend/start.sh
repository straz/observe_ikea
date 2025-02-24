#!/bin/bash
# This script is run once, when the docker container starts up

# Start running the web server in the background
uv run uvicorn main:app --host 0.0.0.0 &

# Ping it once/minute in the background
uv run /app/minicron.py &

# Don't quit docker container. This keeps the background running.
wait
