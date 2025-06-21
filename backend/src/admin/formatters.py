from typing import Any, Optional

from jinja2 import Environment, FileSystemLoader, select_autoescape

from markupsafe import Markup


class BaseTypeFormatter:

    def __init__(self, template_name: str):
        self.template_name = template_name

        self.template_env = Environment(
            loader=FileSystemLoader("templates"),
            autoescape=select_autoescape(["html", "xml"])
        )

    def format(self, value: Any) -> str:
        template = self.template_env.get_template(self.template_name)
        html = template.render(value=value)
        return Markup(html)


class BooleanFormatter(BaseTypeFormatter):

    def __init__(self, template: Optional[str] = None):
        super().__init__(template or "sqladmin/fields/boolean.html")

    def __call__(self, value: bool) -> str:
        return self.format(value)
