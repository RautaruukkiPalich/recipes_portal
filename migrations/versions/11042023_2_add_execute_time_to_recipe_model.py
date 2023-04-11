"""add_execute_time_to_recipe_model

Revision ID: d12326959744
Revises: 840eae126d30
Create Date: 2023-04-11 17:57:18.294991

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd12326959744'
down_revision = '840eae126d30'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('recipe', sa.Column('execute_time', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('recipe', 'execute_time')
    # ### end Alembic commands ###