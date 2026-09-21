"""garantizar un administrador principal por empresa

Revision ID: b5eaa79d5e9f
Revises: 2fc7a8162604
Create Date: 2026-09-21
"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "b5eaa79d5e9f"
down_revision: Union[str, Sequence[str], None] = "2fc7a8162604"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        CREATE UNIQUE INDEX uq_company_principal_admin
        ON company_users (company_id)
        WHERE is_admin = true
        """
    )


def downgrade() -> None:
    op.execute(
        """
        DROP INDEX IF EXISTS uq_company_principal_admin
        """
    )