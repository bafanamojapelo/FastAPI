"""create posts table

Revision ID: 9859ba28384f
Revises: 318cb8f6a965
Create Date: 2024-05-14 03:40:30.963327

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9859ba28384f'
down_revision: Union[str, None] = '318cb8f6a965'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
