import io
from datetime import datetime
from fastapi.responses import StreamingResponse
from weasyprint import HTML
from app.core.templates import TemplateLoader
from app.core.database import SessionDep
from app.modules.members.services import MemberService 
from fastapi import HTTPException, status

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
    async def generate_member_report(session: SessionDep, member_id: int):
        member = await MemberService.get_member_with_details(session, member_id)
        if not member:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Member not found"
            )
        html_string = await TemplateLoader.get_template(
            "pdf/member_report.html",
            member=member,
            fecha=datetime.now().strftime("%d/%m/%Y %H:%M"),
            titulo=f"Extracto de Socio: {member.name} {member.last_name}"
        )
        pdf_bytes = HTML(string=html_string).write_pdf()
        filename = f"Reporte_{member.name}_{member.last_name}.pdf".replace(" ", "_")
        return StreamingResponse(
            io.BytesIO(pdf_bytes),
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename={filename}",
            },
        )