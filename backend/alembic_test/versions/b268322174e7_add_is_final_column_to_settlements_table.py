"""Add is_final column to settlements table

Revision ID: b268322174e7
Revises: 7aab9576ea00
Create Date: 2024-03-19 07:26:36.082006

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b268322174e7'
down_revision: Union[str, None] = '7aab9576ea00'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('settlements', sa.Column('is_final', sa.Boolean(), nullable=False))
    op.add_column('volume_oi', sa.Column('is_final', sa.Boolean(), nullable=False))


def downgrade() -> None:
    op.drop_column('settlements', 'is_final')
    op.drop_column('volume_oi', 'is_final')
