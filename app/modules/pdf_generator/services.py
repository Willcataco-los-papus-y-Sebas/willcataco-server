import io
from datetime import date, datetime
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
    
    @staticmethod
    async def generate_members_water_payments_report(
        session: SessionDep, start_date: date, end_date: date
    ):
        period = await MemberService.get_members_water_payments(session, start_date, end_date)
        if not period:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There is not registers payments in those period")
        html_string = await TemplateLoader.get_template(
            "pdf/members_water_payments_report.html",
            period= period,
            start_date = start_date.strftime("%d/%m/%Y"),
            end_date = end_date.strftime("%d/%m/%Y"),
            fecha= datetime.now().strftime("%d/%m/%Y %H:%M")
        )
        pdf_bytes = HTML(string=html_string).write_pdf()
        filename = f"Reporte_pagos_de_agua_{start_date.isoformat()}_{end_date.isoformat()}.pdf"
        return StreamingResponse(
            io.BytesIO(pdf_bytes),
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename={filename}",
            },
        )

