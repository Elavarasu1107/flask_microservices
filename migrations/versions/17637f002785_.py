"""empty message

Revision ID: 17637f002785
Revises: fe51b36fcb56
Create Date: 2023-08-02 18:01:48.546241

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '17637f002785'
down_revision = 'fe51b36fcb56'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('notes',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('title', sa.String(length=150), nullable=True),
    sa.Column('description', sa.String(length=150), nullable=True),
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('notes', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_notes_id'), ['id'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('notes', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_notes_id'))

    op.drop_table('notes')
    # ### end Alembic commands ###
