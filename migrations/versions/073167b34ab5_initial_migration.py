"""initial migration

Revision ID: 073167b34ab5
Revises: 23dd21320aa8
Create Date: 2021-02-28 15:41:04.222491

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '073167b34ab5'
down_revision = '23dd21320aa8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('phone', sa.String(length=64), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'phone')
    # ### end Alembic commands ###
