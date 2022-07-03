from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from typing import List
from config.config import settings

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_TLS=settings.MAIL_TLS,
    MAIL_SSL=settings.MAIL_SSL,
    USE_CREDENTIALS=settings.USE_CREDENTIALS
)


async def send_email(subject: str, recipient: List, message: str):
    message = MessageSchema(
        subject=subject,
        recipients=recipient,
        body=message,
        subtype="html"
    )
    print(message)
    fm = FastMail(conf)
    await fm.send_message(message)
