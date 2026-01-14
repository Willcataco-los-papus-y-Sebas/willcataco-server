import io

from fastapi.responses import StreamingResponse
from weasyprint import HTML

from app.core.templates import TemplateLoader


class PdfGenService:
    @staticmethod
    async def get_pdf():
        file = await TemplateLoader.get_template("pdf/helloworld.html")
        pdf = HTML(string=file).write_pdf()
        return StreamingResponse(
            io.BytesIO(pdf),
            media_type="application/pdf",
            headers={
                "Content-Disposition": "attachment; filename=helloworld.pdf",
            },
        )
