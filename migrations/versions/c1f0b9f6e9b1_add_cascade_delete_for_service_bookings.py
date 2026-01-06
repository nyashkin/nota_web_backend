"""add cascade delete for service bookings

Revision ID: c1f0b9f6e9b1
Revises: c00d3da268f4
Create Date: 2026-01-03 14:00:00.000000

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = 'c1f0b9f6e9b1'
down_revision: Union[str, Sequence[str], None] = 'c00d3da268f4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_constraint('bookings_service_id_fkey', 'bookings', type_='foreignkey')
    op.create_foreign_key(
        'bookings_service_id_fkey',
        'bookings',
        'services',
        ['service_id'],
        ['id'],
        ondelete='CASCADE',
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('bookings_service_id_fkey', 'bookings', type_='foreignkey')
    op.create_foreign_key(
        'bookings_service_id_fkey',
        'bookings',
        'services',
        ['service_id'],
        ['id'],
    )
