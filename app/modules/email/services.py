from datetime import datetime
from decimal import Decimal
from pydantic import NonNegativeFloat 

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
        name_member: str,
        last_name_member: str,
        ci_member: str,
        id_payment: int,
        water_reading: Decimal,
        date_created: datetime,
        date_updated: datetime,
        amount: NonNegativeFloat 
    ):
        try:
            message = EmailMessage()
            message["From"] = config.email_from
            message["To"] = email.recipient
            message["Subject"] = email.subject
            body = await TemplateLoader.get_template(
                "email/template/water-payments.mjml",
                name = name_member,
                full_name = f'{name_member} {last_name_member}',
                ci = ci_member,
                id_payment = id_payment,
                water_meter = water_reading,
                date_pay = date_created.strftime('%d/%m/%Y'),
                date_paied = date_updated.strftime('%d/%m/%Y'),
                hour_paied = date_updated.strftime('%H:%M'),
                amount = amount
            )
            message.set_content(body, subtype="mjml")
            await email_session.send_message(message)
        except Exception:
            raise