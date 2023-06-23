"""initial table

Revision ID: 9fd67a99519d
Revises: 
Create Date: 2023-06-18 16:02:38.678423

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '9fd67a99519d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('user_name', sa.VARCHAR(length=32), nullable=False),
    sa.Column('chat_id', sa.BigInteger(), nullable=False),
    sa.Column('language', sa.VARCHAR(length=2), nullable=False),
    sa.Column('count_subs', sa.SmallInteger(), nullable=False),
    sa.PrimaryKeyConstraint('user_id')
    )
    op.create_table('services',
    sa.Column('service_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.VARCHAR(length=30), nullable=False),
    sa.Column('months', sa.SmallInteger(), nullable=False),
    sa.Column('reminder', postgresql.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('service_by_user_id', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['service_by_user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('service_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('services')
    op.drop_table('users')
    # ### end Alembic commands ###