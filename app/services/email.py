import aiosmtplib
from email.message import EmailMessage
from app.core.config import settings

async def send_email(
        recipient: str,
        subject: str,
        body: str
):
    message = EmailMessage()

    message['From'] = settings.EMAIL
    message['To'] = recipient
    message['subject'] = subject

    message.set_content(body)

    await aiosmtplib.send(
        message,
        hostname="smtp.gmail.com",
        port=587,
        username=settings.EMAIL,
        password=settings.PASSWORD,
        start_tls=True
    )

