"""login delete

Revision ID: ed2a01f047d4
Revises: 7a0e283e2cfa
Create Date: 2023-02-06 13:40:37.801087

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'ed2a01f047d4'
down_revision = '7a0e283e2cfa'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_users_id', table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('password', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('first_name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('second_name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='users_pkey')
    )
    op.create_index('ix_users_id', 'users', ['id'], unique=False)
    # ### end Alembic commands ###
