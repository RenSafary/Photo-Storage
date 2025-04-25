import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv


def send_message(to_email, reset_link):
    load_dotenv()

    SMTP_SERVER = os.getenv("SMTP_SERVER")
    SMTP_PORT = os.getenv("SMTP_PORT")
    EMAIL = os.getenv("EMAIL")
    PASSWORD = os.getenv("PASSWORD")

    msg = EmailMessage()
    msg.set_content(f"Click on the link to recover your password:\n{reset_link}")
    msg["From"] = EMAIL
    msg["Subject"] = "Password recover"
    msg["To"] = to_email

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL, PASSWORD)
        server.send_message(msg)
