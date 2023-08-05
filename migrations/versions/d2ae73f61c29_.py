"""empty message

Revision ID: d2ae73f61c29
Revises: 17637f002785
Create Date: 2023-08-03 18:02:09.422703

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd2ae73f61c29'
down_revision = '17637f002785'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('collaborator',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('note_id', sa.BigInteger(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('collaborator', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_collaborator_id'), ['id'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('collaborator', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_collaborator_id'))

    op.drop_table('collaborator')
    # ### end Alembic commands ###
