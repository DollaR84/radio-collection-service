from datetime import datetime, timedelta, timezone
from typing import Any, Optional, Type

from application.types import UserAccessRights

from db.models import AccessPermission

from sqladmin import ModelView

from starlette.requests import Request
from starlette.datastructures import FormData

from wtforms import Form, IntegerField


class AccessPermissionAdmin(ModelView, model=AccessPermission):
    name = "Access Permission"
    name_plural = "Access Permissions"

    column_list = [
        "id",
        "user",
        "access_rights",
        "reason",
        "created_at",
        "expires_at",
    ]

    form_columns = [
        "user",
        "access_rights",
        "reason",
        "created_at",
        "expires_at",
    ]

    form_args = {
        "access_rights": {
            "choices": [
                (permission.name, permission.value)
                for permission in UserAccessRights
                if permission != UserAccessRights.OWNER
            ]
        }
    }

    column_labels = {
        "access_rights": "Access Rights",
        "expires_at": "Expiration Date",
    }

    _access_expire_days: dict[UserAccessRights, int] = {}

    async def scaffold_form(self, rules: Optional[Any] = None) -> Type[Form]:
        form_cls = await super().scaffold_form(rules)

        if not hasattr(form_cls, "extend_days"):
            form_cls.extend_days = IntegerField(
                "Extend by (days)",
                default=0,
                description="Number of days to extend access",
            )

        return form_cls

    async def on_model_change(
            self,
            data: dict[str, Any],
            model: AccessPermission,
            is_created: bool,
            request: Request,
    ) -> None:
        if not is_created and model.access_rights == UserAccessRights.OWNER:
            raise ValueError("can not change Owner!")

        form_data: FormData = await request.form()
        extend_days_raw = form_data.get("extend_days", "0")

        match extend_days_raw:
            case str():
                try:
                    extend_days = int(extend_days_raw)
                except ValueError:
                    extend_days = 0

            case _:
                extend_days = 0

        if is_created and extend_days:
            data["expires_at"] = datetime.now(timezone.utc) + timedelta(days=extend_days)
        elif extend_days:
            if model.expires_at and model.expires_at > datetime.now(timezone.utc):
                data["expires_at"] = model.expires_at + timedelta(days=extend_days)
            else:
                data["expires_at"] = datetime.now(timezone.utc) + timedelta(days=extend_days)

        await super().on_model_change(data, model, is_created, request)
