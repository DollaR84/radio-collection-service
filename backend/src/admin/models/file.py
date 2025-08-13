from db.models import File

from sqladmin import ModelView
from sqladmin.filters import ForeignKeyFilter

from ..formatters import BooleanFormatter


class FileAdmin(ModelView, model=File):
    name = "File"
    name_plural = "Files"
    icon = "fa-solid fa-star"

    column_list = [
        "id",
        "user",
        "filename",
        "fileext",
        "is_load",
        "created_at",
    ]

    column_details_list = [
        "user.user_name",
        "user.email",
        "file_id",
        "file_path",
        "filename",
        "fileext",
        "is_load",
        "created_at",
    ]

    form_columns = [
        "user_id",
        "file_id",
        "file_path",
        "filename",
        "fileext",
        "is_load",
        "created_at",
    ]

    column_labels = {
        "user_id": "User ID",
    }

    column_searchable_list = [
        "user.email",
        "fileext",
        "is_load",
    ]

    column_sortable_list = [
        "created_at",
        "user_id",
    ]

    form_ajax_refs = {
        "user": {
            "fields": ("email", "user_name",),
            "order_by": "email",
        },
    }

    column_type_formatters = {
        bool: BooleanFormatter(),
    }

    column_filters = [
        ForeignKeyFilter(File.user_id, File.user.user_name, title="User Name"),
    ]
