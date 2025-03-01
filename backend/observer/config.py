# Enter your local configuration data here

from .home import Home

HOMES = [
    Home(
        ip="198.168.x.x",
        token="""eyJhbG...zzzz""",
    )
]


SENDMAIL_CONFIG = {
    "myself": "yourname@example.com",
    "host": "smtp-relay.example.com",
    "port": 587,
}
