from datetime import datetime
from email.message import EmailMessage

from app.core.config import config
from app.core.email import EmailSession
from app.core.templates import TemplateLoader
from app.modules.email.schemas import (
    EmailBase,
    EmailWaterReceiptBase,
    WaterBillEmailParams,
)


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
                "email/internal_login.html",
                url=url,
                expire_time=str(expire_time),
                email_title="Acceso Administracion",
                year=str(datetime.now().year),
            )
            message.set_content(body, subtype="html")
            await email_session.send_message(message)
        except Exception:
            raise

    @staticmethod
    async def send_water_bill_email(
        email_session: EmailSession,
        bill_data: WaterBillEmailParams,
    ):
        try:
            message = EmailMessage()
            message["From"] = config.email_from
            message["To"] = bill_data.recipient
            message["Subject"] = bill_data.subject
            template_context = bill_data.model_dump()
            template_context["date"] = bill_data.date.strftime("%Y-%m-%d")
            template_context["reading_value"] = f"{bill_data.reading_value:.2f}"

            body = await TemplateLoader.get_template(
                "email/notificacion_boleta.html",
                email_title=bill_data.subject,
                year=str(datetime.now().year),
                **template_context,
            )
            message.set_content(body, subtype="html")
            await email_session.send_message(message)
        except Exception:
            raise

    @staticmethod
    async def send_water_payment_email(
        email_session: EmailSession,
        email: EmailBase,
        email_receipt: EmailWaterReceiptBase,
    ):
        try:
            message = EmailMessage()
            message["From"] = config.email_from
            message["To"] = email.recipient
            message["Subject"] = email.subject

            dump_receipt = email_receipt.model_dump()
            dump_receipt["date_created"] = email_receipt.date_created.strftime(
                "%d/%m/%Y"
            )
            dump_receipt["date_updated"] = email_receipt.date_updated.strftime(
                "%d/%m/%Y  %H:%M"
            )

            body = await TemplateLoader.get_template(
                "email/water_payment.html",
                **dump_receipt,
                email_title="Recibo del agua",
                year=str(datetime.now().year),
            )
            message.set_content(body, subtype="html")
            await email_session.send_message(message)
        except Exception:
            raise
