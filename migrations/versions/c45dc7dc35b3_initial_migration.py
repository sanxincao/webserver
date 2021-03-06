"""initial migration

Revision ID: c45dc7dc35b3
Revises: 75ff2d53a4c2
Create Date: 2021-03-04 12:24:16.204690

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c45dc7dc35b3'
down_revision = '75ff2d53a4c2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('servers', sa.Column('isbaned', sa.Boolean(), nullable=True))
    op.add_column('servers', sa.Column('isselect', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('servers', 'isselect')
    op.drop_column('servers', 'isbaned')
    # ### end Alembic commands ###
