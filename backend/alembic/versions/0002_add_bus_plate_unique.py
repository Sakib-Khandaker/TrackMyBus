from alembic import op


revision = "0002_add_bus_plate_unique"
down_revision = "0001_initial"
branch_labels = None
depends_on = None


def upgrade():
    op.create_index(
        "ix_buses_plate_number",
        "buses",
        ["plate_number"],
        unique=True,
    )


def downgrade():
    op.drop_index("ix_buses_plate_number", table_name="buses")
