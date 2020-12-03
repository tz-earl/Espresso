"""empty message

Revision ID: e8040589fbad
Revises: 3927aa9ff189
Create Date: 2020-12-02 16:52:24.273044

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e8040589fbad'
down_revision = '3927aa9ff189'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('restaurant', sa.Column('creator', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('restaurant', 'creator')
    # ### end Alembic commands ###
