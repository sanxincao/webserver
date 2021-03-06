"""initial migration

Revision ID: 23dd21320aa8
Revises: aa79b1808989
Create Date: 2021-02-28 15:40:27.500646

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '23dd21320aa8'
down_revision = 'aa79b1808989'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'phone')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('phone', mysql.INTEGER(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
