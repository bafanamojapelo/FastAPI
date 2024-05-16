"""add last few columns to posts table

Revision ID: 83c8f9511b70
Revises: 700e1ce73ed4
Create Date: 2024-05-14 12:39:56.620075

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '83c8f9511b70'
down_revision: Union[str, None] = '700e1ce73ed4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts',sa.Column(
        'published', sa.Boolean(), nullable=False, server_default='TRUE'),)
    op.add_column('posts',sa.Column(
        'create_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')),)
    pass


def downgrade():
    op.drop_column('posts','published')
    op.drop_column('posts','create_at')
    pass
