"""Add asset, settlement, and volume_oi tables

Revision ID: 36949b7c298c
Revises: ce6916ff562d
Create Date: 2024-02-27 13:21:44.007239

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '36949b7c298c'
down_revision: Union[str, None] = 'ce6916ff562d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('assets',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('name', sa.String(length=64), nullable=False, unique=True)
    )
    op.create_table('settlements',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('asset_id', sa.Integer(), sa.ForeignKey('assets.id'), nullable=False),
        sa.Column('trade_date', sa.Date(), nullable=False),
        sa.Column('month', sa.String(length=16), nullable=False),
        sa.Column('open', sa.String(length=16)),
        sa.Column('high', sa.String(length=16)),
        sa.Column('low', sa.String(length=16)),
        sa.Column('last', sa.String(length=16)),
        sa.Column('change', sa.Float(precision=2)),
        sa.Column('settle', sa.Float(precision=2), nullable=False),
        sa.Column('est_volume', sa.Integer(), nullable=False),
        sa.Column('prior_day_oi', sa.Integer(), nullable=False),
        sa.UniqueConstraint('asset_id', 'trade_date', 'month', name='_asset_date_month_uc')
    )
    op.create_table('volume_oi',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('asset_id', sa.Integer(), sa.ForeignKey('assets.id'), nullable=False),
        sa.Column('trade_date', sa.Date(), nullable=False),
        sa.Column('month', sa.String(length=16), nullable=False),
        sa.Column('globex', sa.Integer()),
        sa.Column('open_outcry', sa.Integer()),
        sa.Column('clear_port', sa.Integer()),
        sa.Column('total_volume', sa.Integer(), nullable=False),
        sa.Column('block_trades', sa.Integer()),
        sa.Column('efp', sa.Integer()),
        sa.Column('efr', sa.Integer()),
        sa.Column('tas', sa.Integer()),
        sa.Column('deliveries', sa.Integer()),
        sa.Column('at_close', sa.Integer()),
        sa.Column('change', sa.Integer()),
        sa.UniqueConstraint('asset_id', 'trade_date', 'month', name='_asset_date_month_uc')
    )


def downgrade() -> None:
    op.drop_table('volume_oi')
    op.drop_table('settlements')
    op.drop_table('assets')
