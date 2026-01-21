from jinja2 import Environment, FileSystemLoader, PrefixLoader
from pathlib import Path
from typing import Any

class TemplateLoader:
    __email_templates = Path(__file__).parent.parent / "modules" / "email" / "templates" / "html"
    __pdf_templates = Path(__file__).parent.parent / "modules" / "pdf_generator" / "templates"

    __jinja_env = Environment(
        loader=PrefixLoader({
            'email': FileSystemLoader(str(__email_templates)),
            'pdf': FileSystemLoader(str(__pdf_templates)),
        }),
        autoescape=True,
        enable_async=True
    )

    @staticmethod
    async def get_template(template_name: str, **kwargs: Any) -> str:
        try:
            template = TemplateLoader.__jinja_env.get_template(template_name)
            return await template.render_async(kwargs)
        except Exception:            
            raise