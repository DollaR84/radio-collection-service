from typing import TYPE_CHECKING

import sqlalchemy as sa
import sqlalchemy.orm as so

from ..base import Base
from ..mixins import TimeCreateMixin

if TYPE_CHECKING:
    from .user import User


class File(TimeCreateMixin, Base):

    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    user: so.Mapped["User"] = so.relationship("User", foreign_keys=[user_id], back_populates="files")

    file_id: so.Mapped[str] = so.mapped_column(sa.String, unique=True, nullable=False)
    file_path: so.Mapped[str] = so.mapped_column(sa.String, nullable=False)

    filename: so.Mapped[str] = so.mapped_column(sa.String, nullable=False)
    fileext: so.Mapped[str] = so.mapped_column(sa.String(5), nullable=False)

    is_load: so.Mapped[bool] = so.mapped_column(default=False)
