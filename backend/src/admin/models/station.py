from typing import Any, Optional, Type

from db.models import Station

from sqladmin import ModelView

from starlette.requests import Request

from wtforms import Form, StringField


class StationAdmin(ModelView, model=Station):
    name = "Station"
    name_plural = "Stations"
    icon = "fa-solid fa-tower-cell"

    column_list = [
        "id",
        "name",
        "tags",
        "status",
    ]

    form_columns = [
        "name",
        "url",
        "tags",
        "status",
    ]

    form_widget_args = {
        "url": {
            "readonly": True,
        },
    }

    form_extra_fields = {
        "tags": StringField(
            "Tags",
            render_kw={
                "data-role": "tags-manager",
                "class": "tags-input",
                "aria-label": "Tags input field",
                "aria-describedby": "tags-help",
                "autocomplete": "off",
                "role": "textbox",
                "aria-multiline": "false",
                "aria-autocomplete": "list",
                "aria-haspopup": "listbox",
                "inputmode": "text",
                "tabindex": "0",
            },
        )
    }

    async def scaffold_form(self, rules: Optional[Any] = None) -> Type[Form]:
        form_class = await super().scaffold_form(rules)

        form_class.tags = StringField(
            "Tags",
            render_kw={
                "data-role": "tags-manager",
                "class": "tags-input",
                "aria-label": "Tags input field",
                "aria-describedby": "tags-help",
                "autocomplete": "off",
                "role": "textbox",
                "aria-multiline": "false",
                "aria-autocomplete": "list",
                "aria-haspopup": "listbox",
                "inputmode": "text",
                "tabindex": "0",
            },
        )

        if rules and hasattr(rules, "tags"):
            form_class.tags.data = ", ".join(rules.tags or [])  # type: ignore[attr-defined]

        return form_class

    async def on_model_change(
        self,
        data: dict[str, Any],
        model: Station,
        is_created: bool,
        request: Request,
    ) -> None:
        if "tags" in data:
            model.tags = [tag.strip() for tag in data["tags"].split(",") if tag.strip()]

        await super().on_model_change(data, model, is_created, request)
