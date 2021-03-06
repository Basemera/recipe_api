"""empty message

Revision ID: cad69bb23cae
Revises: 3ce59fc8948f
Create Date: 2018-01-06 15:00:44.914705

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cad69bb23cae'
down_revision = '3ce59fc8948f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('blacklist',
    sa.Column('number', sa.Integer(), nullable=False),
    sa.Column('datecreated', sa.DateTime(), nullable=True),
    sa.Column('userid', sa.Integer(), nullable=False),
    sa.Column('blacklist', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('number')
    )
    op.create_index(op.f('ix_blacklist_blacklist'), 'blacklist', ['blacklist'], unique=True)
    op.create_index(op.f('ix_blacklist_userid'), 'blacklist', ['userid'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_blacklist_userid'), table_name='blacklist')
    op.drop_index(op.f('ix_blacklist_blacklist'), table_name='blacklist')
    op.drop_table('blacklist')
    # ### end Alembic commands ###
