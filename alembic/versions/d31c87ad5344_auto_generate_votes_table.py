"""auto generate votes table

Revision ID: d31c87ad5344
Revises: ca8d294d6710
Create Date: 2025-03-04 22:51:42.391734

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd31c87ad5344'
down_revision: Union[str, None] = 'ca8d294d6710'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
