"""add_source_to_transmitters

Revision ID: 3f5d2c1b7e1c
Revises: 9b7c2f8d3e1a
Create Date: 2026-02-05 00:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "3f5d2c1b7e1c"
down_revision: str | None = "9b7c2f8d3e1a"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    with op.batch_alter_table("transmitters", schema=None) as batch_op:
        batch_op.add_column(sa.Column("source", sa.String(), nullable=True))


def downgrade() -> None:
    with op.batch_alter_table("transmitters", schema=None) as batch_op:
        batch_op.drop_column("source")
