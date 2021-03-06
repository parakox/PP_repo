"""empty message

Revision ID: a55c6c16765a
Revises: c3e9142692a2
Create Date: 2020-12-08 18:35:05.173677

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a55c6c16765a'
down_revision = 'c3e9142692a2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('professors', sa.Column('username', sa.String(), nullable=True))
    op.create_foreign_key(None, 'professors', 'users', ['username'], ['username'])
    op.add_column('students', sa.Column('username', sa.String(), nullable=True))
    op.create_foreign_key(None, 'students', 'users', ['username'], ['username'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'students', type_='foreignkey')
    op.drop_column('students', 'username')
    op.drop_constraint(None, 'professors', type_='foreignkey')
    op.drop_column('professors', 'username')
    # ### end Alembic commands ###
