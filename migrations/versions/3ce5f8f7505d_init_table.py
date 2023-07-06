"""init table

Revision ID: 3ce5f8f7505d
Revises: 
Create Date: 2023-07-05 16:30:09.074795

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3ce5f8f7505d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('services',
    sa.Column('service_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(length=30), nullable=False),
    sa.Column('months', sa.SmallInteger(), nullable=False),
    sa.Column('reminder', sa.DateTime(), nullable=False),
    sa.Column('service_by_user_id', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['service_by_user_id'], ['users.user_id'], name=op.f('services_service_by_user_id_fkey')),
    sa.PrimaryKeyConstraint('service_id', name=op.f('pk__services'))
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('services')
    # ### end Alembic commands ###