from typing import TYPE_CHECKING

import sqlalchemy as sa
import sqlalchemy.orm as so

from application.types import StationStatusType

from ..base import Base
from ..mixins import TimeCreateMixin, TimeUpdateMixin

if TYPE_CHECKING:
    from .favorite import Favorite


class Station(TimeCreateMixin, TimeUpdateMixin, Base):

    name: so.Mapped[str] = so.mapped_column(sa.String, nullable=False)
    url: so.Mapped[str] = so.mapped_column(sa.String, unique=True, nullable=False)

    tags: so.Mapped[list[str]] = so.mapped_column(
        sa.ARRAY(sa.String(50)),
        default=list,
        nullable=False,
    )

    status: so.Mapped[StationStatusType] = so.mapped_column(
        sa.Enum(StationStatusType, name="station_status_type", create_constraint=True, validate_strings=True),
        default=StationStatusType.NOT_VERIFIED,
        nullable=False,
        index=True,
    )

    __table_args__ = (
        sa.Index("ix_tags_gin", tags, postgresql_using="gin"),
    )

    favorites: so.Mapped["Favorite"] = so.relationship("Favorite", back_populates="station")
