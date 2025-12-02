"""add orders and order_items tables

Revision ID: 6ed508b9f5ba
Revises: 839beaff6b74
Create Date: 2025-12-02 12:12:03.536868

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6ed508b9f5ba'
down_revision: Union[str, Sequence[str], None] = '839beaff6b74'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Création des tables Orders et OrderItems UNIQUEMENT
    op.create_table(
        'orders',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey("users.id")),
        sa.Column('total_price', sa.Float(), nullable=False),
        sa.Column('status', sa.String(), nullable=False, default="pending"),
        sa.Column('created_at', sa.DateTime(), nullable=False)
    )

    op.create_table(
        'order_items',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('order_id', sa.Integer(), sa.ForeignKey("orders.id")),
        sa.Column('product_id', sa.Integer(), sa.ForeignKey("products.id")),
        sa.Column('quantity', sa.Integer(), nullable=False),
        sa.Column('price', sa.Float(), nullable=False)
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('order_items')
    op.drop_table('orders')
