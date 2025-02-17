"""Create table apps

Revision ID: fd3318b17e0c
Revises: 
Create Date: 2024-07-16 20:56:36.765182

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fd3318b17e0c'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('apps',
    sa.Column('UUID', sa.UUID(), nullable=False),
    sa.Column('kind', sa.String(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('version', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('state', sa.String(), nullable=True),
    sa.Column('json', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('UUID'),
    sa.UniqueConstraint('name')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('apps')
    # ### end Alembic commands ###
