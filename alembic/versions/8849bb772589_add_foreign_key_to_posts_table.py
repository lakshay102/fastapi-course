"""add foreign-key to posts table

Revision ID: 8849bb772589
Revises: e52afb482705
Create Date: 2025-03-04 07:56:14.265593

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "8849bb772589"
down_revision: Union[str, None] = "e52afb482705"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("owner_id", sa.Integer(), nullable=False))
    op.create_foreign_key(
        "posts_users_fkey",
        source_table="posts",
        referent_table="users",
        local_cols=["owner_id"],
        remote_cols=["id"],
        ondelete="CASCADE",
    )
    pass


def downgrade() -> None:
    op.drop_constraint("posts_users_fkey", table_name= "posts")
    op.drop_column("posts","owner_id")
    pass
