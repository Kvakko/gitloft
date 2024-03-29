"""empty message

Revision ID: 71a2dddf4d59
Revises: 267cbf583d49
Create Date: 2020-04-02 14:05:36.949769

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '71a2dddf4d59'
down_revision = '267cbf583d49'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('forestilling', sa.Column('aktuell', sa.Boolean(), nullable=True))
    op.create_index(op.f('ix_forestilling_aktuell'), 'forestilling', ['aktuell'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_forestilling_aktuell'), table_name='forestilling')
    op.drop_column('forestilling', 'aktuell')
    # ### end Alembic commands ###
