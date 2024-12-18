"""add active plan

Revision ID: a131452a1770
Revises: 3589ef050779
Create Date: 2024-12-16 08:23:07.543322

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a131452a1770'
down_revision: Union[str, None] = '3589ef050779'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('planmodel')
    op.drop_table('customermodel')
    op.drop_table('transactionmodel')
    op.drop_table('customerplanlink')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('customerplanlink',
    sa.Column('customer_id', sa.INTEGER(), nullable=False),
    sa.Column('plan_id', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['customer_id'], ['customermodel.id'], ),
    sa.ForeignKeyConstraint(['plan_id'], ['planmodel.id'], ),
    sa.PrimaryKeyConstraint('customer_id', 'plan_id')
    )
    op.create_table('transactionmodel',
    sa.Column('amount', sa.FLOAT(), nullable=True),
    sa.Column('description', sa.VARCHAR(), nullable=True),
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('date', sa.DATETIME(), nullable=False),
    sa.Column('customer_id', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['customer_id'], ['customermodel.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('customermodel',
    sa.Column('name', sa.VARCHAR(), nullable=False),
    sa.Column('description', sa.VARCHAR(), nullable=True),
    sa.Column('email', sa.VARCHAR(), nullable=False),
    sa.Column('age', sa.INTEGER(), nullable=False),
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('planmodel',
    sa.Column('name', sa.VARCHAR(), nullable=False),
    sa.Column('description', sa.VARCHAR(), nullable=True),
    sa.Column('price', sa.FLOAT(), nullable=False),
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('active', sa.BOOLEAN(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
