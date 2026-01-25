from typing import Annotated

from aiosmtplib import SMTP
from fastapi import Depends

from app.core.config import config


async def get_email_session():
    smtp = SMTP(
        hostname=config.smtp_server,
        port=config.smtp_port,
        use_tls=config.smtp_use_tls,
        start_tls=config.smtp_start_tls,
    )

    try:
        await smtp.connect()
        await smtp.starttls()
        await smtp.login(config.email_sender, config.email_sender_password)
        yield smtp
    except Exception:
        raise
    finally:
        try:
            await smtp.quit()
        except Exception:
            smtp.close()


EmailSession = Annotated[SMTP, Depends(get_email_session)]
