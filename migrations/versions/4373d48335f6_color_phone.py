"""color phone

Revision ID: 4373d48335f6
Revises: ad164e55f222
Create Date: 2023-06-11 19:36:14.789253

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4373d48335f6'
down_revision = 'ad164e55f222'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('item', schema=None) as batch_op:
        batch_op.add_column(sa.Column('about_model', sa.String(length=1000), nullable=True))
        batch_op.alter_column('color',
               existing_type=sa.VARCHAR(length=1000),
               type_=sa.String(length=100),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('item', schema=None) as batch_op:
        batch_op.alter_column('color',
               existing_type=sa.String(length=100),
               type_=sa.VARCHAR(length=1000),
               existing_nullable=True)
        batch_op.drop_column('about_model')

    # ### end Alembic commands ###