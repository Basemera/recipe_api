"""empty message

Revision ID: 758aff125a69
Revises: 2d59357c477e
Create Date: 2017-12-17 22:58:13.126184

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '758aff125a69'
down_revision = '2d59357c477e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('recipe_category', sa.Column('user', sa.Integer(), nullable=True))
    op.drop_constraint('recipe_category_owner_fkey', 'recipe_category', type_='foreignkey')
    op.create_foreign_key(None, 'recipe_category', 'user', ['user'], ['userid'])
    op.drop_column('recipe_category', 'owner')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('recipe_category', sa.Column('owner', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'recipe_category', type_='foreignkey')
    op.create_foreign_key('recipe_category_owner_fkey', 'recipe_category', 'user', ['owner'], ['userid'])
    op.drop_column('recipe_category', 'user')
    # ### end Alembic commands ###