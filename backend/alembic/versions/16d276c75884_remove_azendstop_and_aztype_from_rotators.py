"""remove azendstop and aztype from rotators

Revision ID: 16d276c75884
Revises: 5eef1a43935a
Create Date: 2025-10-26 10:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "16d276c75884"
down_revision: str | None = "5eef1a43935a"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # Remove azendstop and aztype columns from rotators table
    op.drop_column("rotators", "azendstop")
    op.drop_column("rotators", "aztype")


def downgrade() -> None:
    # Re-add azendstop and aztype columns if downgrading
    op.add_column("rotators", sa.Column("aztype", sa.Integer(), nullable=False, server_default="0"))
    op.add_column(
        "rotators", sa.Column("azendstop", sa.Integer(), nullable=False, server_default="0"),
    )
