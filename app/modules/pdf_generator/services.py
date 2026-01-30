import io
from datetime import date, datetime
from typing import List

from fastapi import HTTPException, status
from fastapi.responses import StreamingResponse
from weasyprint import HTML

from app.core.database import SessionDep
from app.core.enums import PaymentStatus
from app.core.templates import TemplateLoader
from app.modules.extra_payments.extra_payments.services import ExtraPaymentService
from app.modules.extra_payments.payments.services import PaymentService
from app.modules.members.services import MemberService
from app.modules.water_meters.water_payments.services import WaterPaymentService

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

        filename = (
            f"new_members_report_{start_date.isoformat()}_{end_date.isoformat()}.pdf"
        )

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
                status_code=status.HTTP_404_NOT_FOUND, detail="Member not found"
            )
        html_string = await TemplateLoader.get_template(
            "pdf/member_report.html",
            member=member,
            fecha=datetime.now().strftime("%d/%m/%Y %H:%M"),
            titulo=f"Extracto de Socio: {member.name} {member.last_name}",
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
    async def get_receipt_extra_payment(session: SessionDep, payment_id: int):
        payment = await PaymentService.get_payment_by_id(session, payment_id)
        if not payment:
            raise HTTPException(detail="payment not found", status_code=400)
        if payment.status is PaymentStatus.UNPAID:
            raise HTTPException(detail="payment is unpaid", status_code=400)
        extra = await ExtraPaymentService.get_by_id(session, payment.extra_payment_id)
        member = await MemberService.get_member_by_id(session, payment.member_id)
        fecha = payment.created_at.strftime("%d/%m/%Y %H:%M")
        html_string = await TemplateLoader.get_template(
            "pdf/receipt_extra_payment.html",
            member=member,
            extra=extra,
            fecha=datetime.now().strftime("%d/%m/%Y %H:%M"),
            date=fecha,
            payment=payment,
        )
        pdf_bytes = HTML(string=html_string).write_pdf()
        filename = f"Recibo_{member.name}_del_{fecha}.pdf".replace(" ", "_")
        return StreamingResponse(
            io.BytesIO(pdf_bytes),
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename={filename}",
            },
        )

    @staticmethod
    async def get_receipt_water_payment(session: SessionDep, payment_ids: List[int]):
        payments = await WaterPaymentService.get_payments_by_ids(session, payment_ids)
        if not payments:
            raise HTTPException(detail="No payments found", status_code=404)
        first_member_id = payments[0].member_id
        total_amount = 0
        for p in payments:
            if p.member_id != first_member_id:
                raise HTTPException(detail="All payments must belong to the same member", status_code=400)
            if p.status == PaymentStatus.UNPAID:
                raise HTTPException(detail=f"Payment {p.id} is unpaid", status_code=400)
            total_amount += p.amount
        fecha_emision = datetime.now().strftime("%d/%m/%Y %H:%M")
        html_string = await TemplateLoader.get_template(
            "pdf/receipt_water_payment.html",
            payments=payments,
            total_amount=total_amount,
            fecha_emision=fecha_emision,
            fecha=fecha_emision 
        )
        if len(payments) > 1:
            filename = f"Recibo_Agua_{payments[0].member.last_name}_mult.pdf"
        else:
            filename = f"Recibo_Agua_{payments[0].member.last_name}_{payments[0].id}.pdf"
        pdf_bytes = HTML(string=html_string).write_pdf()
        return StreamingResponse(
            io.BytesIO(pdf_bytes),
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename={filename}",
            },
        )