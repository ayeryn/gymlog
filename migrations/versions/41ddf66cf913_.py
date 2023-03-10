"""empty message

Revision ID: 41ddf66cf913
Revises: 0d7e0a852b59
Create Date: 2023-03-10 17:16:28.768707

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '41ddf66cf913'
down_revision = '0d7e0a852b59'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('attendance', schema=None) as batch_op:
        batch_op.add_column(sa.Column('test_field', sa.Integer(), nullable=True))

    with op.batch_alter_table('gym_class', schema=None) as batch_op:
        batch_op.alter_column('class_type',
               existing_type=sa.VARCHAR(length=20),
               type_=sa.String(length=3),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('gym_class', schema=None) as batch_op:
        batch_op.alter_column('class_type',
               existing_type=sa.String(length=3),
               type_=sa.VARCHAR(length=20),
               existing_nullable=True)

    with op.batch_alter_table('attendance', schema=None) as batch_op:
        batch_op.drop_column('test_field')

    # ### end Alembic commands ###
