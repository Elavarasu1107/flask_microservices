"""empty message

Revision ID: 27fd5afc2dfc
Revises: d2ae73f61c29
Create Date: 2023-08-05 17:24:06.135600

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils

# revision identifiers, used by Alembic.
revision = '27fd5afc2dfc'
down_revision = 'd2ae73f61c29'
branch_labels = None
depends_on = None


def upgrade():
    access = [
        ('writable', 'WRITABLE'),
        ('read_only', 'READ-ONLY')
    ]
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('collaborator', schema=None) as batch_op:
        batch_op.add_column(sa.Column('access_type', sqlalchemy_utils.types.choice.ChoiceType(access),
                                      nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('collaborator', schema=None) as batch_op:
        batch_op.drop_column('access_type')

    # ### end Alembic commands ###
