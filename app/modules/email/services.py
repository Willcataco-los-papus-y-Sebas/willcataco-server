from datetime import datetime

from email.message import EmailMessage

from app.core.config import config
from app.core.email import EmailSession
from app.core.templates import TemplateLoader
from app.modules.email.schemas import EmailBase, EmailWaterReceiptBase


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
    async def send_water_payment_email(
        email_session: EmailSession,
        email: EmailBase,
        email_receipt: EmailWaterReceiptBase 
    ):
        try:
            message = EmailMessage()
            message["From"] = config.email_from
            message["To"] = email.recipient
            message["Subject"] = email.subject
            body = await TemplateLoader.get_template(
                "email/water_payment.html",
                name = email_receipt.name_member,
                full_name = f'{email_receipt.name_member} {email_receipt.last_name_member}',
                ci = email_receipt.ci_member,
                id_payment = email_receipt.id_payment,
                water_meter = email_receipt.water_reading,
                date_pay = email_receipt.date_created.strftime('%d/%m/%Y'),
                date_paied = email_receipt.date_updated.strftime('%d/%m/%Y'),
                hour_paied = email_receipt.date_updated.strftime('%H:%M'),
                amount = email_receipt.amount
            )
            message.set_content(body, subtype="html")
            await email_session.send_message(message)
        except Exception:
            raise