"""
Send a message to myself, using the Google SMTP relay.

No auth is needed because I'm sending to myself.

Configure SMTP server with whitelisted IP address:
https://support.google.com/a/answer/176600?hl=en&fl=1&sjid=18241002030510003695-NA
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from .config import SMTP_USER, SMTP_HOST, SMTP_PORT


def make_msg(message: str, subject: str):
    msg = MIMEMultipart()
    msg["From"] = SMTP_USER
    msg["To"] = SMTP_USER
    msg["Subject"] = subject
    msg.attach(MIMEText(message, "plain"))  # or 'html'
    return msg


def send_mail(message: str, subject: str):
    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.send_message(make_msg(message, subject))
    except Exception as e:
        print(f"Error sending email: {e}")
