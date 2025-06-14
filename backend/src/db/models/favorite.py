import sqlalchemy as sa
import sqlalchemy.orm as so

from ..base import Base
from ..mixins import TimeCreateMixin


class Favorite(TimeCreateMixin, Base):

    id: so.Mapped[int] = so.mapped_column(
        primary_key=False,
        autoincrement=True,
        server_default=sa.Sequence('favorites_id_seq').next_value()
    )

    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    station_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("stations.id", ondelete="CASCADE"), primary_key=True)
