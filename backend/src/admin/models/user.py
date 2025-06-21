from typing import Any, Optional, Type

from application.services import Resolver
from application.types import UserAccessRights

from db.models import User

from sqladmin import ModelView

from starlette.requests import Request

from wtforms import Form

from ..formatters import BooleanFormatter


class UserAdmin(ModelView, model=User):
    name = "User"
    name_plural = "Users"

    column_list = [
        "id",
        "uuid_id",
        "google_id",
        "email",
        "user_name",
        "first_name",
        "last_name",
        "access_rights",
        "is_active",
        "is_admin",
        "created_at",
        "updated_at",
        "access_permissions",
    ]

    form_columns = [
        "email",
        "user_name",
        "first_name",
        "last_name",
        "access_rights",
        "is_active",
        "is_admin",
    ]

    form_args = {
        "access_rights": {
            "choices": [
                (level.value, level.name)
                for level in UserAccessRights
                if level != UserAccessRights.OWNER
            ]
        }
    }

    column_labels = {
        "email": "eMail",
        "access_rights": "Access rights now",
        "access_permissions": "List of access permissions",
    }

    column_details_list = [
        *column_list,
        "access_permissions.reason",
        "access_permissions.expires_at",
    ]

    form_ajax_refs = {
        "access_permissions": {
            "fields": ("reason", "expires_at"),
            "order_by": "expires_at",
        }
    }

    column_type_formatters = {
        bool: BooleanFormatter(),
    }

    async def scaffold_form(self, rules: Optional[Any] = None) -> Type[Form]:
        form = await super().scaffold_form(rules)

        if rules and hasattr(rules, "access_rights") and hasattr(form, "access_rights"):
            if rules.access_rights == UserAccessRights.OWNER:
                form.access_rights.render_kw = {"disabled": True}

        return form

    async def on_model_change(
            self,
            data: dict[str, Any],
            model: User,
            is_created: bool,
            request: Request,
    ) -> None:
        if not is_created and model.access_rights == UserAccessRights.OWNER and "access_rights" in data:
            data.pop("access_rights")

        await super().on_model_change(data, model, is_created, request)

        if "access_rights" in data:
            if data["access_rights"] == UserAccessRights.OWNER:
                raise ValueError("no one can be appointed as the owner")

            if data["access_rights"] != UserAccessRights.DEFAULT:
                await self._create_access_permission(model, request)

    async def _create_access_permission(self, model: User, request: Request) -> None:
        resolver = await request.state.container.get(Resolver)
        await resolver.create(model.id, model.access_rights)
