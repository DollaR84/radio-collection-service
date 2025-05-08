import sqlalchemy as sa
import sqlalchemy.orm as so

from application.types import StationStatusType

from ..base import Base
from ..mixins import TimeCreateMixin, TimeUpdateMixin


class Station(TimeCreateMixin, TimeUpdateMixin, Base):

    name: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=False)
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
