"""add wishlist_items table

Revision ID: 839beaff6b74
Revises: b1624d710f42
Create Date: 2025-12-02 12:00:00.861613

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '839beaff6b74'
down_revision: Union[str, Sequence[str], None] = 'b1624d710f42'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Création de la table wishlist_items UNIQUEMENT
    op.create_table(
        'wishlist_items',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey("users.id")),
        sa.Column('product_id', sa.Integer(), sa.ForeignKey("products.id"))
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('wishlist_items')
