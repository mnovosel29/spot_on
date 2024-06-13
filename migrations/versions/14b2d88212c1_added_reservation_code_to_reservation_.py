"""Added reservation code to reservation table.

Revision ID: 14b2d88212c1
Revises: 2e5881ea0f56
Create Date: 2024-06-13 09:34:19.223261

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '14b2d88212c1'
down_revision = '2e5881ea0f56'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('reservation', schema=None) as batch_op:
        batch_op.add_column(sa.Column('reservation_code', sa.String(length=255), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('reservation', schema=None) as batch_op:
        batch_op.drop_column('reservation_code')

    # ### end Alembic commands ###
