"""empty message

Revision ID: 3686a5b98e09
Revises: c4da8b5e50ec
Create Date: 2018-01-05 17:05:46.810177

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3686a5b98e09'
down_revision = 'c4da8b5e50ec'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_users_lastname', table_name='users')
    op.drop_column('users', 'lastname')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('lastname', sa.VARCHAR(length=100), autoincrement=False, nullable=False))
    op.create_index('ix_users_lastname', 'users', ['lastname'], unique=False)
    # ### end Alembic commands ###
