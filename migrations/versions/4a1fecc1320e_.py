"""empty message

Revision ID: 4a1fecc1320e
Revises: 8e0bf3aa991b
Create Date: 2023-08-07 15:13:46.097995

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils as su


# revision identifiers, used by Alembic.
revision = '4a1fecc1320e'
down_revision = '8e0bf3aa991b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('note_label',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('note_id', sa.BigInteger(), nullable=False),
    sa.Column('label_id', sa.BigInteger(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('note_label', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_note_label_id'), ['id'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('note_label', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_note_label_id'))

    op.drop_table('note_label')
    # ### end Alembic commands ###
