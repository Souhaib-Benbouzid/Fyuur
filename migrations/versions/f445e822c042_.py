"""empty message

Revision ID: f445e822c042
Revises: 15a011a69e0a
Create Date: 2020-01-18 08:55:01.755947

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f445e822c042'
down_revision = '15a011a69e0a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'state', ['id', 'state'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'state', type_='unique')
    # ### end Alembic commands ###
