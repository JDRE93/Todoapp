"""empty message

Revision ID: b30e86bafc8d
Revises: 7d9d74f37080
Create Date: 2025-07-02 22:01:36.879743

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b30e86bafc8d'
down_revision = '7d9d74f37080'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('task', schema=None) as batch_op:
        batch_op.add_column(sa.Column('fecha_vencimiento', sa.DateTime(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('task', schema=None) as batch_op:
        batch_op.drop_column('fecha_vencimiento')

    # ### end Alembic commands ###
