from app.core.config import config
import asyncio
from email.message import EmailMessage
from app.core.email import EmailSession
from app.modules.email.schemas import EmailBase

class EmailService:
    @staticmethod
    async def send_email(email_session : EmailSession, email : EmailBase):
        try:
            message = EmailMessage()
            message["From"] = config.email_sender
            message["To"] = email.recipient
            message["Subject"] = email.subject
            message.set_content(email.body)
            await email_session.send_message(message)
        except Exception:
            raise
