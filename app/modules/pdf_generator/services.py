from fastapi.responses import StreamingResponse
from weasyprint import HTML
import io

class PdfGenService:
    @staticmethod
    async def get_pdf():
        file = await PdfGenService.read_pdf()
        pdf = HTML(string=file).write_pdf()
        return StreamingResponse(
            io.BytesIO(pdf),
            media_type="application/pdf",
            headers={
                "Content-Disposition": "attachment; filename=helloworld.pdf",
            }
        )


    @staticmethod
    async def read_pdf(path : str = "./app/modules/pdf_generator/templates/helloworld.html"):
        try:
            with open(path, mode="r", encoding="utf-8") as file:
                html_temp = file.read()
            return html_temp
        except FileNotFoundError:
            raise 