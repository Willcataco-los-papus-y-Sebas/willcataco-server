from email.message import EmailMessage

from app.core.config import config
from app.core.email import EmailSession
from app.core.templates import TemplateLoader
from app.modules.email.schemas import EmailBase


class EmailService:
    @staticmethod
    async def send_email(email_session: EmailSession, email: EmailBase):
        try:
            message = EmailMessage()
            message["From"] = config.email_from
            message["To"] = email.recipient
            message["Subject"] = email.subject
            body = await TemplateLoader.get_template("email/email_test.html")
            message.set_content(body, subtype="html")
            await email_session.send_message(message)
        except Exception:
            raise

    @staticmethod
    async def send_reset_pass_email(
        email_session: EmailSession, email: EmailBase, url: str
    ):
        try:
            message = EmailMessage()
            message["From"] = config.email_from
            message["To"] = email.recipient
            message["Subject"] = email.subject
            body = await TemplateLoader.get_template(
                "email/reset_password.html", url=url
            )
            message.set_content(body, subtype="html")
            await email_session.send_message(message)
        except Exception:
            raise
