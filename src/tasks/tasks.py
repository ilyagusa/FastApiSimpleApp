import smtplib
from email.message import EmailMessage

from celery import Celery
from config import SMTP_USER, SMTP_PASS

SMTP_HOST = "smtp.yandex.com"
SMTP_PORT = 465

celery = Celery('tasks', broker='redis://localhost:6379')


@celery.task
def send_email_report(username: str):
    email_msg = EmailMessage()
    email_msg.set_content(f"Hello world {username}")
    email_msg["Subject"] = "Hello world"
    email_msg["From"] = SMTP_USER
    email_msg["To"] = SMTP_USER

    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(email_msg)

