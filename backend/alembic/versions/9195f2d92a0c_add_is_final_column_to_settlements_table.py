"""Add is_final column to settlements and volume_oi tables

Revision ID: 9195f2d92a0c
Revises: 36949b7c298c
Create Date: 2024-03-19 07:20:14.102180

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9195f2d92a0c'
down_revision: Union[str, None] = '36949b7c298c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('settlements', sa.Column('is_final', sa.Boolean(), nullable=False))
    op.add_column('volume_oi', sa.Column('is_final', sa.Boolean(), nullable=False))


def downgrade() -> None:
    op.drop_column('settlements', 'is_final')
    op.drop_column('volume_oi', 'is_final')
