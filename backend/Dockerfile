# build this image with
# docker build -t automax .

# run with
# docker run -it -p 8000:8000 -v ./data:/app/data automax

# Python version should match .python-version
FROM python:3.12

RUN apt update && apt -y upgrade
WORKDIR /app

COPY . /app
RUN pip install uv
RUN uv sync


# This starts two long-running jobs:
#   1. main.py (web server)
#   2. minicron.py (ping the web server every minute)
CMD ["/app/start.sh"]
