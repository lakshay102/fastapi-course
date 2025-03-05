"""add content column to posts table

Revision ID: 577e77546a81
Revises: 2fd9e30ee098
Create Date: 2025-03-03 22:37:50.962987

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '577e77546a81'
down_revision: Union[str, None] = '2fd9e30ee098'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('content', sa.String(), nullable= False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
