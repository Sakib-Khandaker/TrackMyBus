from alembic import op
import sqlalchemy as sa

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(120), nullable=False),
        sa.Column("email", sa.String(255), nullable=False),
        sa.Column("password_hash", sa.Text(), nullable=False),
        sa.Column("role", sa.String(30), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)

    op.create_table(
        "buses",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("code", sa.String(50), nullable=False),
        sa.Column("plate_number", sa.String(50), nullable=False),
        sa.Column("capacity", sa.Integer(), nullable=False, server_default="40"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
    )
    op.create_index("ix_buses_code", "buses", ["code"], unique=True)

    op.create_table(
        "routes",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(150), nullable=False),
        sa.Column("start_point", sa.String(150), nullable=False),
        sa.Column("end_point", sa.String(150), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
    )

    op.create_table(
        "locations",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("bus_id", sa.Integer(), sa.ForeignKey("buses.id"), nullable=False),
        sa.Column("latitude", sa.Float(), nullable=False),
        sa.Column("longitude", sa.Float(), nullable=False),
        sa.Column("speed_kmh", sa.Float(), nullable=False, server_default="0"),
        sa.Column("heading", sa.Float(), nullable=False, server_default="0"),
        sa.Column("recorded_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_locations_bus_id", "locations", ["bus_id"])
    op.create_index("ix_locations_recorded_at", "locations", ["recorded_at"])

def downgrade():
    op.drop_table("locations")
    op.drop_table("routes")
    op.drop_index("ix_buses_code", table_name="buses")
    op.drop_table("buses")
    op.drop_index("ix_users_email", table_name="users")
    op.drop_table("users")
