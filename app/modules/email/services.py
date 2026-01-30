from datetime import datetime
from email.message import EmailMessage

from app.core.config import config
from app.core.email import EmailSession
from app.core.templates import TemplateLoader
from app.modules.email.schemas import EmailBase, ExtraPaymentEmailParams


class EmailService:
    @staticmethod
    async def send_email(email_session: EmailSession, email: EmailBase):
        try:
            message = EmailMessage()
            message["From"] = config.email_from
            message["To"] = email.recipient
            message["Subject"] = email.subject
            body = await TemplateLoader.get_template(
                "email/template.html",
                email_title=email.subject,
                year=str(datetime.now().year),
            )
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

    @staticmethod
    async def send_extra_payment_email(
        email_session: EmailSession,
        payment_data: ExtraPaymentEmailParams,
    ):
        message = EmailMessage()
        message["From"] = config.email_from
        message["To"] = payment_data.recipient
        message["Subject"] = payment_data.subject
        template_context = payment_data.model_dump()
        template_context["payment_date"] = payment_data.payment_date.strftime("%Y-%m-%d")
        template_context["amount"] = f"{payment_data.amount:.2f}"
        
        body = await TemplateLoader.get_template(
            "email/confirmacion_pago_extra.mjml",
            email_title=payment_data.subject,
            year=str(datetime.now().year),
            **template_context,
        )
        message.set_content(body, subtype="html")
        await email_session.send_message(message)
