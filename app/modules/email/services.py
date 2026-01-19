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
            body = await TemplateLoader.get_template("email/template.html", head_title=email.subject)
            message.set_content(body, subtype="html")
            await email_session.send_message(message)
        except Exception:
            raise

    @staticmethod
    async def send_reset_pass_email(
        email_session: EmailSession,
        email: EmailBase,
        url: str,
        expire_time: int = config.reset_token_time_expire,
    ):
        try:
            message = EmailMessage()
            message["From"] = config.email_from
            message["To"] = email.recipient
            message["Subject"] = email.subject
            body = await TemplateLoader.get_template(
                "email/reset_password.html", url=url, expire_time=str(expire_time)
            )
            message.set_content(body, subtype="html")
            await email_session.send_message(message)
        except Exception:
            raise

    @staticmethod
    async def send_internal_login_email(
        email_session: EmailSession,
        email: EmailBase,
        url: str,
        expire_time: int,
    ):
        try:
            message = EmailMessage()
            message["From"] = config.email_from
            message["To"] = email.recipient
            message["Subject"] = email.subject
            body = await TemplateLoader.get_template(
                "email/internal_login.html", url=url, expire_time=str(expire_time)
            )
            message.set_content(body, subtype="html")
            await email_session.send_message(message)
        except Exception:
            raise
