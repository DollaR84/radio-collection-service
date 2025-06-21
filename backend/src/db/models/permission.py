from datetime import datetime
from typing import Optional, TYPE_CHECKING

import sqlalchemy as sa
import sqlalchemy.orm as so

from application.types import UserAccessRights

from ..base import Base
from ..mixins import TimeCreateMixin

if TYPE_CHECKING:
    from .user import User


class AccessPermission(TimeCreateMixin, Base):

    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("users.id", ondelete="CASCADE"), index=True)
    reason: so.Mapped[Optional[str]] = so.mapped_column(sa.String, nullable=True)

    access_rights: so.Mapped[UserAccessRights] = so.mapped_column(
        sa.Enum(UserAccessRights, name="user_access_rights", create_constraint=True, validate_strings=True),
        nullable=False,
    )

    expires_at: so.Mapped[datetime] = so.mapped_column(
        sa.DateTime(timezone=True),
        nullable=False,
    )

    user: so.Mapped["User"] = so.relationship("User", foreign_keys=[user_id], back_populates="access_permissions")
