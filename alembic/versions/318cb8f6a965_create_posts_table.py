"""create posts table

Revision ID: 318cb8f6a965
Revises: 
Create Date: 2024-05-10 20:23:02.819689

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision='318cb8f6a965'
down_revision= None
branch_labels= None
depends_on= None


def upgrade():
    op.create_table(
        'posts',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('title', sa.String, nullable=False),
        sa.Column('content', sa.Text, nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now())
    )

def downgrade():
    op.drop_table('posts')