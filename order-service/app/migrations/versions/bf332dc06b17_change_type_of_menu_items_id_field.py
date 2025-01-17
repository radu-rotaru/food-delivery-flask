"""Change type of menu_items_id field

Revision ID: bf332dc06b17
Revises: d49df3c743c9
Create Date: 2025-01-16 20:27:17.355326

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'bf332dc06b17'
down_revision = 'd49df3c743c9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('order', schema=None) as batch_op:
        batch_op.alter_column('menu_items_ids',
               existing_type=postgresql.BYTEA(),
               type_=sa.String(length=1000),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('order', schema=None) as batch_op:
        batch_op.alter_column('menu_items_ids',
               existing_type=sa.String(length=1000),
               type_=postgresql.BYTEA(),
               existing_nullable=True)

    # ### end Alembic commands ###
