# Enter your local configuration data here

LOCAL_TZ = "America/New_York"

# Local path inside your Dockerfile
LOGFILE = "/var/log/gather.log"

HOMES = [
    {
        "ip": "198.168.x.x",
        "token": "eyJhbG...zzzz",
    }
]

SMTP_USER = "yourname@example.com"
SMTP_HOST = "smtp-relay.example.com"
SMTP_PORT = 587
