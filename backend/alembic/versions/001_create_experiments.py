"""create experiments

Revision ID: 001
Revises:
Create Date: 2026-10-06
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "experiments",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(500), nullable=False, index=True),
        sa.Column("dataset", sa.String(500), nullable=False, index=True),
        sa.Column("model_name", sa.String(500), nullable=False, index=True),
        sa.Column("status", sa.String(50), nullable=False, index=True, server_default="planned"),
        sa.Column("accuracy", sa.Float(), nullable=True),
        sa.Column("duration_sec", sa.Float(), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
    )


def downgrade() -> None:
    op.drop_table("experiments")
