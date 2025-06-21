from datetime import datetime, timedelta, timezone
from typing import Any

from application.types import UserAccessRights

from db.models import AccessPermission

from sqladmin import ModelView

from starlette.requests import Request

from wtforms import IntegerField


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

    form_extra_fields = {
        "extend_days": IntegerField(
            "Extend by (days)",
            default=7,
            description="Number of days to extend access",
        )
    }

    form_columns = [
        "user",
        "access_rights",
        "reason",
        "expires_at",
        "extend_days",
    ]

    form_args = {
        "access_rights": {
            "choices": [
                (permission.value, permission.name)
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

    async def on_model_change(
            self,
            data: dict[str, Any],
            model: AccessPermission,
            is_created: bool,
            request: Request,
    ) -> None:
        if not is_created and model.access_rights == UserAccessRights.OWNER:
            raise ValueError("can not change Owner!")

        extend_days = data.get("extend_days", 7)
        if is_created:
            model.expires_at = datetime.now(timezone.utc) + timedelta(days=extend_days)
        else:
            if model.expires_at and model.expires_at > datetime.now(timezone.utc):
                model.expires_at += timedelta(days=extend_days)
            else:
                model.expires_at = datetime.now(timezone.utc) + timedelta(days=extend_days)

        await super().on_model_change(data, model, is_created, request)
