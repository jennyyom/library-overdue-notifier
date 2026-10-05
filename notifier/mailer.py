"""Send email, or just print it when we are testing (dry run)."""

import os
import smtplib
from email.message import EmailMessage

from notifier.messages import Reminder


def print_reminder(reminder: Reminder) -> None:
    print("=" * 60)
    print(f"To: {reminder.member_name} <{reminder.email}>")
    print(f"Subject: {reminder.subject}")
    print()
    print(reminder.body)


def send_reminders(reminders: list[Reminder]) -> None:
    """Send through an SMTP server (Gmail by default).

    The password is read from an environment variable, never written in the code.
    For Gmail, create an "App Password" and use that here.
    """
    host = os.environ.get("SMTP_HOST", "smtp.gmail.com")
    port = int(os.environ.get("SMTP_PORT", "587"))
    user = os.environ["SMTP_USER"]
    password = os.environ["SMTP_PASSWORD"]

    with smtplib.SMTP(host, port) as server:
        server.starttls()
        server.login(user, password)
        for reminder in reminders:
            message = EmailMessage()
            message["From"] = user
            message["To"] = reminder.email
            message["Subject"] = reminder.subject
            message.set_content(reminder.body)
            server.send_message(message)
