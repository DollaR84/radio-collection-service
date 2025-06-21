from typing import TYPE_CHECKING

import sqlalchemy as sa
import sqlalchemy.orm as so

from ..base import Base
from ..mixins import TimeCreateMixin

if TYPE_CHECKING:
    from .station import Station
    from .user import User


class Favorite(TimeCreateMixin, Base):

    id: so.Mapped[int] = so.mapped_column(
        primary_key=False,
        autoincrement=True,
        server_default=sa.Sequence('favorites_id_seq').next_value()
    )

    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    station_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("stations.id", ondelete="CASCADE"), primary_key=True)

    user: so.Mapped["User"] = so.relationship("User", foreign_keys=[user_id], back_populates="favorites")
    station: so.Mapped["Station"] = so.relationship("Station", foreign_keys=[station_id], back_populates="favorites")
