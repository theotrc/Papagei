"""size

Revision ID: 3ac60ca83ed1
Revises: 220ebd34d05a
Create Date: 2023-06-11 17:11:39.999782

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3ac60ca83ed1'
down_revision = '220ebd34d05a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('item_size', schema=None) as batch_op:
        batch_op.alter_column('size',
               existing_type=sa.VARCHAR(length=10),
               type_=sa.String(length=100),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('item_size', schema=None) as batch_op:
        batch_op.alter_column('size',
               existing_type=sa.String(length=100),
               type_=sa.VARCHAR(length=10),
               existing_nullable=True)

    # ### end Alembic commands ###
