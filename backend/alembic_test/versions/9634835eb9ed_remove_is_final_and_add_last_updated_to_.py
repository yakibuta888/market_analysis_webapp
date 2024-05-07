"""Remove is_final and add last_updated to settlements

Revision ID: 9634835eb9ed
Revises: b268322174e7
Create Date: 2024-05-07 02:45:49.365328

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func


# revision identifiers, used by Alembic.
revision: str = '9634835eb9ed'
down_revision: Union[str, None] = 'b268322174e7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # `is_final` カラムを削除
    bind = op.get_bind().engine
    inspector = sa.inspect(bind)
    columns = [column['name'] for column in inspector.get_columns('settlements')]
    if 'is_final' in columns:
        op.drop_column('settlements', 'is_final')
    # `last_updated` カラムを追加
    op.add_column('settlements', sa.Column('last_updated', sa.DateTime(), nullable=False, server_default=func.now()))


def downgrade() -> None:
    # `is_final` カラムを再追加
    op.add_column('settlements', sa.Column('is_final', sa.Boolean(), nullable=False, server_default=sa.sql.expression.false()))
    # `last_updated` カラムを削除
    bind = op.get_bind().engine
    inspector = sa.inspect(bind)
    columns = [column['name'] for column in inspector.get_columns('settlements')]
    if 'last_updated' in columns:
        op.drop_column('settlements', 'last_updated')
