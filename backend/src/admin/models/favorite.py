from db.models import Favorite

from sqladmin import ModelView
from sqladmin.filters import DateTimeBetween, ForeignKeyFilter


class FavoriteAdmin(ModelView, model=Favorite):
    name = "Favorite"
    name_plural = "Favorites"
    icon = "fa-solid fa-star"

    column_list = [
        "id",
        "user",
        "station",
        "created_at",
    ]

    column_details_list = [
        "user.user_name",
        "user.email",
        "station.name",
        "created_at",
    ]

    form_columns = [
        "user",
        "station",
    ]

    column_labels = {
        "user_id": "User ID",
        "station_id": "Station ID",
        "created_at": "Favorited At",
    }

    column_searchable_list = [
        "user.email",
        "station.name",
    ]

    column_sortable_list = [
        "created_at",
        "user.email",
        "station.name",
    ]

    column_filters = [
        ForeignKeyFilter(Favorite.user_id, Favorite.user.user_name, title="User Name"),
        ForeignKeyFilter(Favorite.station_id, Favorite.station.name, title="Station Name"),
        DateTimeBetween(column="created_at", name="Created Between"),
    ]

    form_ajax_refs = {
        "user": {
            "fields": ("email", "user_name",),
            "order_by": "email",
        },
        "station": {
            "fields": ("name", "status",),
            "order_by": "name",
        },
    }
