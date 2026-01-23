import io
from datetime import date, datetime

from fastapi.responses import StreamingResponse
from weasyprint import HTML

from app.core.database import SessionDep
from app.core.templates import TemplateLoader
from app.modules.members.services import MemberService


class PdfGenService:
    @staticmethod
    async def get_pdf():
        file = await TemplateLoader.get_template("pdf/helloworld.html")
        pdf = HTML(string=file).write_pdf()
        return StreamingResponse(
            io.BytesIO(pdf),
            media_type="application/pdf",
            headers={"Content-Disposition": "attachment; filename=helloworld.pdf"},
        )

    @staticmethod
    async def get_new_members_report(
        session: SessionDep,
        start_date: date,
        end_date: date,
    ):
        members = await MemberService.get_new_members_between_dates(
            session, start_date, end_date
        )
        total = len(members)

        generated_at = datetime.now().strftime("%d/%m/%Y %H:%M")

        html = await TemplateLoader.get_template(
            "pdf/new_members_report.html",
            fecha=generated_at,
            start_date=start_date.strftime("%d/%m/%Y"),
            end_date=end_date.strftime("%d/%m/%Y"),
            total=total,
            members=members,
        )

        pdf = HTML(string=html).write_pdf()

        filename = f"new_members_report_{start_date.isoformat()}_{end_date.isoformat()}.pdf"

        return StreamingResponse(
            io.BytesIO(pdf),
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={filename}"},
        )
