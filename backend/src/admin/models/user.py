from typing import Any

from application.services import Resolver
from application.types import UserAccessRights

from db.models import User

from sqladmin import ModelView

from starlette.requests import Request

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

    column_formatters = {
        "access_rights": lambda model, name: model.access_rights.name if model.access_rights else "",
        "access_permissions": lambda model, name: ", ".join([
            f"{p.access_rights.name} (expires {p.expires_at.strftime('%Y-%m-%d') if p.expires_at else 'never'})"
            for p in model.access_permissions
        ]) if model.access_permissions else "",
        "created_at": (
            lambda model, name:
                model.created_at.strftime("%Y-%m-%d %H:%M") if model.created_at else ""
        ),
        "updated_at": (
            lambda model, name:
                model.updated_at.strftime("%Y-%m-%d %H:%M") if model.updated_at else ""
        ),
    }

    async def on_model_change(
            self,
            data: dict[str, Any],
            model: User,
            is_created: bool,
            request: Request,
    ) -> None:
        old_rights = getattr(model, "access_rights", None)

        access_rights_value = data.get("access_rights")
        new_rights = UserAccessRights[access_rights_value] if access_rights_value else old_rights

        if not is_created and old_rights == UserAccessRights.OWNER and new_rights:
            data.pop("access_rights")
            new_rights = old_rights

        await super().on_model_change(data, model, is_created, request)

        if not is_created and new_rights and new_rights != UserAccessRights.DEFAULT and new_rights != old_rights:
            await self._create_access_permission(model.id, new_rights, request)

    async def _create_access_permission(self, user_id: int, access_rights: UserAccessRights, request: Request) -> None:
        if access_rights == UserAccessRights.DEFAULT:
            return

        async with request.state.container() as container:
            resolver = await container.get(Resolver)
            await resolver.create(user_id, access_rights)
