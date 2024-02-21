"""'delete_category'

Revision ID: f65933732993
Revises: 1d1437f07573
Create Date: 2024-02-21 10:27:51.727842

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'f65933732993'
down_revision: Union[str, None] = '1d1437f07573'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('category')
    op.drop_column('transaction_families', 'transaction_category')
    op.drop_column('transaction_users', 'transaction_category')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('transaction_users', sa.Column('transaction_category', sa.INTEGER(), autoincrement=False, nullable=False))
    op.add_column('transaction_families', sa.Column('transaction_category', sa.INTEGER(), autoincrement=False, nullable=False))
    op.create_table('category',
    sa.Column('category_id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('family_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('category_name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('category_id', name='category_pkey')
    )
    # ### end Alembic commands ###
