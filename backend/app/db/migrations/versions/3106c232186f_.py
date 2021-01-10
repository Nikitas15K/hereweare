"""

Revision ID: 3106c232186f
Revises: 
Create Date: 2020-12-27 10:47:17.796899

"""
from typing import Tuple
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic
revision = '3106c232186f'
down_revision = None
branch_labels = None
depends_on = None


def create_updated_at_trigger() -> None:
    op.execute(
        """
        CREATE OR REPLACE FUNCTION update_updated_at_column()
            RETURNS TRIGGER AS
        $$
        BEGIN
            NEW.updated_at = now();
            RETURN NEW;
        END;
        $$ language 'plpgsql';
        """
    )


def timestamps() -> Tuple[sa.Column, sa.Column]:
    return (
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )


def create_vehicles_table() -> None:
    op.create_table(
        "vehicles",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("sign", sa.Text, nullable=False, index=True, unique=True),
        sa.Column("type", sa.Text, nullable=False, server_default="car"),
        sa.Column("model", sa.Text, nullable=False),
        sa.Column("manufacture_year", sa.Integer, nullable=False),
        *timestamps(),
    )
    op.execute(
        """
        CREATE TRIGGER update_vehicle_modtime
            BEFORE UPDATE
            ON vehicles
            FOR EACH ROW
        EXECUTE PROCEDURE update_updated_at_column();
        """
    )

def create_insurance_company_table() -> None:
    op.create_table(
        "insurance_company",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.Text, nullable=False, index=True, unique=True),
        sa.Column("email", sa.Text, nullable=False),
        *timestamps(),
    )
    op.execute(
        """
        CREATE TRIGGER update_insurance_company_modtime
            BEFORE UPDATE
            ON insurance_company
            FOR EACH ROW
        EXECUTE PROCEDURE update_updated_at_column();
        """

    )


def create_insurance_table() -> None:
    op.create_table(
        "insurance",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("number", sa.Text, nullable=False, index=True, unique=True),
        sa.Column("expire_date", sa.BigInteger, nullable=False),
        sa.Column("vehicle_id", sa.Integer, sa.ForeignKey('vehicles.id')),
        sa.Column("insurance_company_id", sa.Integer, sa.ForeignKey('insurance_company.id')),
        *timestamps(),
    )
    op.execute(
        """
        CREATE TRIGGER update_insurance_modtime
            BEFORE UPDATE
            ON insurance
            FOR EACH ROW
        EXECUTE PROCEDURE update_updated_at_column();
        """
    )


def create_users_table() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("username", sa.Text, unique=True, nullable=False, index=True),
        sa.Column("email", sa.Text, unique=True, nullable=False, index=True),
        sa.Column("email_verified", sa.Boolean, nullable=False, server_default="False"),
        sa.Column("salt", sa.Text, nullable=False),
        sa.Column("password", sa.Text, nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="True"),
        sa.Column("is_superuser", sa.Boolean(), nullable=False, server_default="False"),
        *timestamps(),
    )
    op.execute(
        """
        CREATE TRIGGER update_user_modtime
            BEFORE UPDATE
            ON users
            FOR EACH ROW
        EXECUTE PROCEDURE update_updated_at_column();
        """
    )

def create_profiles_table() -> None:
    op.create_table(
        "profiles",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("first_name", sa.Text, nullable=True),
        sa.Column("last_name", sa.Text, nullable=True),
        sa.Column("phone_number", sa.Text, nullable=True),
        sa.Column("licence_number", sa.Text, nullable=True),
        sa.Column("licence_category", sa.Text, nullable=True),
        sa.Column("licence_expire_date", sa.BigInteger, nullable=True),
        sa.Column("image", sa.Text, nullable=True),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE")),
        *timestamps(),
    )
    op.execute(
        """
        CREATE TRIGGER update_profiles_modtime
            BEFORE UPDATE
            ON profiles
            FOR EACH ROW
        EXECUTE PROCEDURE update_updated_at_column();
        """
    )


def upgrade() -> None:
    create_updated_at_trigger()
    create_vehicles_table()
    create_insurance_company_table()
    create_users_table()
    create_insurance_table()
    create_profiles_table()


def downgrade() -> None:
    op.drop_table("profiles")
    op.drop_table('insurance_company')
    op.drop_table("users")
    op.drop_table('vehicles')
    op.drop_table('insurance')
    op.execute("DROP FUNCTION update_updated_at_column")



