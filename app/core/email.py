from typing import Annotated

from aiosmtplib import SMTP
from fastapi import Depends

from app.core.config import config


async def get_email_session():
    smtp = SMTP(hostname=config.smtp_server, port=config.smtp_port)

    try:
        await smtp.connect()
        await smtp.starttls()
        await smtp.login(config.smtp_user, config.smtp_password)
        yield smtp
    except Exception:
        raise
    finally:
        try:
            await smtp.quit()
        except Exception:
            smtp.close()


EmailSession = Annotated[SMTP, Depends(get_email_session)]
