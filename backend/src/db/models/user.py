from __future__ import annotations

from typing import Optional, TYPE_CHECKING
import uuid

import sqlalchemy as sa
import sqlalchemy.orm as so
from sqlalchemy.dialects.postgresql import UUID as PgUUID

from ..base import Base
from ..mixins import TimeCreateMixin, TimeUpdateMixin

if TYPE_CHECKING:
    from db.models.station import Station


class User(TimeCreateMixin, TimeUpdateMixin, Base):

    uuid_id: so.Mapped[uuid.UUID] = so.mapped_column(
        PgUUID(as_uuid=True),
        unique=True,
        nullable=False,
        default=uuid.uuid4,
    )
    google_id: so.Mapped[Optional[str]] = so.mapped_column(sa.String(21), unique=True, nullable=True)

    email: so.Mapped[str] = so.mapped_column(sa.String(254), unique=True, nullable=False)
    hashed_password: so.Mapped[Optional[str]] = so.mapped_column(sa.String(60), nullable=True)

    user_name: so.Mapped[Optional[str]] = so.mapped_column(sa.String(50), nullable=True)
    first_name: so.Mapped[Optional[str]] = so.mapped_column(sa.String(100), nullable=True)
    last_name: so.Mapped[Optional[str]] = so.mapped_column(sa.String(100), nullable=True)

    is_active: so.Mapped[bool] = so.mapped_column(default=True)
    is_admin: so.Mapped[bool] = so.mapped_column(default=False)

    favorite_stations: so.Mapped[list["Station"]] = so.relationship(
        secondary="favorites",
        back_populates="favorited_by",
        lazy="selectin",
        viewonly=True,
    )
