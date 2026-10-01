"""add route to bus relationship

Revision ID: 95d604efb9d1
Revises: 0001_initial
Create Date: 2026-09-28
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "95d604efb9d1"
down_revision: Union[str, Sequence[str], None] = "0001_initial"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "buses",
        sa.Column("route_id", sa.Integer(), nullable=True),
    )

    op.create_foreign_key(
        "fk_buses_route_id_routes",
        "buses",
        "routes",
        ["route_id"],
        ["id"],
    )

    op.create_index(
        "ix_buses_route_id",
        "buses",
        ["route_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_buses_route_id", table_name="buses")

    op.drop_constraint(
        "fk_buses_route_id_routes",
        "buses",
        type_="foreignkey",
    )

    op.drop_column("buses", "route_id")