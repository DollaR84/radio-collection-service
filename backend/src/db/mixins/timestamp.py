from datetime import datetime

import sqlalchemy as sa
import sqlalchemy.orm as so


class TimeCreateMixin:

    created_at: so.Mapped[datetime] = so.mapped_column(
        sa.DateTime(timezone=True),
        server_default=sa.func.now(),  # pylint: disable=not-callable
        nullable=False,
    )


class TimeUpdateMixin:

    updated_at: so.Mapped[datetime] = so.mapped_column(
        sa.DateTime(timezone=True),
        server_default=sa.func.now(),  # pylint: disable=not-callable
        onupdate=sa.func.now(),  # pylint: disable=not-callable
        nullable=False,
    )
