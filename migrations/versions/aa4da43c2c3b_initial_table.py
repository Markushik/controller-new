"""initial table

Revision ID: aa4da43c2c3b
Revises: 
Create Date: 2023-06-03 13:48:57.184947

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aa4da43c2c3b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('services',
    sa.Column('service_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.VARCHAR(length=30), nullable=False),
    sa.Column('reminder', sa.Date(), nullable=False),
    sa.PrimaryKeyConstraint('service_id')
    )
    op.create_table('users',
    sa.Column('user_id', sa.BigInteger(), nullable=True),
    sa.Column('user_name', sa.VARCHAR(length=120), nullable=False),
    sa.Column('chat_id', sa.BigInteger(), nullable=False),
    sa.PrimaryKeyConstraint('user_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    op.drop_table('services')
    # ### end Alembic commands ###
