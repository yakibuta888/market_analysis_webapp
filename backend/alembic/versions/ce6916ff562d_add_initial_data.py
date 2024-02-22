"""Add initial data

Revision ID: ce6916ff562d
Revises: bf08bf5eff2d
Create Date: 2024-02-19 12:29:19.406243

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from sqlalchemy import String

from src.domain.value_objects.password import Password


# revision identifiers, used by Alembic.
revision: str = 'ce6916ff562d'
down_revision: Union[str, None] = 'bf08bf5eff2d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # テーブルオブジェクトの定義
    users_table = table('users',
        column('email', String),
        column('hashed_password', String),
        column('name', String)
    )

    # ハッシュ化されたパスワードを生成
    hashed_password_user1 = Password.create("user1password").hashed_password
    hashed_password_user2 = Password.create("user2password").hashed_password
    hashed_password_user3 = Password.create("user3password").hashed_password

    # 初期データを挿入
    op.bulk_insert(users_table,
        [
            {'email': 'user1@example.com', 'hashed_password': hashed_password_user1, 'name': 'User One'},
            {'email': 'user2@example.com', 'hashed_password': hashed_password_user2, 'name': 'User Two'},
            {'email': 'user3@example.com', 'hashed_password': hashed_password_user3, 'name': 'User Three'}
        ]
    )


def downgrade() -> None:
    # SQLAlchemy の table と column を使って users テーブルを定義
    users_table = sa.table('users',
        sa.column('email', sa.String)
    )

    # 削除するメールアドレスのリスト
    emails_to_delete = ['user1@example.com', 'user2@example.com', 'user3@example.com']

    # 安全に特定のユーザーを削除
    op.execute(
        users_table.delete().where(users_table.c.email.in_(emails_to_delete))
    )
