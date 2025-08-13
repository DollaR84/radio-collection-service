from typing import Optional, TYPE_CHECKING
import uuid

import sqlalchemy as sa
import sqlalchemy.orm as so
from sqlalchemy.dialects.postgresql import UUID as PgUUID

from application.types import UserAccessRights

from ..base import Base
from ..mixins import TimeCreateMixin, TimeUpdateMixin

if TYPE_CHECKING:
    from .favorite import Favorite
    from .file import File
    from .permission import AccessPermission


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

    access_rights: so.Mapped[UserAccessRights] = so.mapped_column(
        sa.Enum(UserAccessRights, name="user_access_rights", create_constraint=True, validate_strings=True),
        default=UserAccessRights.DEFAULT,
        server_default=UserAccessRights.DEFAULT.name,
        nullable=False,
    )

    access_permissions: so.Mapped[list["AccessPermission"]] = so.relationship(
        "AccessPermission", back_populates="user",
        cascade="all, delete-orphan", uselist=True
    )
    favorites: so.Mapped[list["Favorite"]] = so.relationship(
        "Favorite", back_populates="user",
        cascade="all, delete-orphan", uselist=True
    )
    files: so.Mapped[list["File"]] = so.relationship(
        "File", back_populates="user",
        cascade="all, delete-orphan", uselist=True
    )
