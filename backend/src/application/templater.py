from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader


class Templater:

    def __init__(self) -> None:
        self.extension = "template"

        path = Path(Path(__file__).parent.parent, "templates").resolve()
        self.loader = FileSystemLoader(path)
        self.env = Environment(loader=self.loader, trim_blocks=True, lstrip_blocks=True)

    def __call__(self, name: str, **kwargs: Any) -> str:
        template_name = f"{name}.{self.extension}"
        template = self.env.get_template(template_name)

        return template.render(**kwargs)
