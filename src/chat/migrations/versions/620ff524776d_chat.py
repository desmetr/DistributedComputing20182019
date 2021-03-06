"""chat

Revision ID: 620ff524776d
Revises: 
Create Date: 2019-05-18 23:13:15.005466

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '620ff524776d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('chat',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user1', sa.String(), nullable=True),
    sa.Column('user2', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('chat_history',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('chatID', sa.Integer(), nullable=False),
    sa.Column('timeStamp', sa.DateTime(), nullable=False),
    sa.Column('message', sa.String(), nullable=False),
    sa.Column('userID', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('chat_history')
    op.drop_table('chat')
    # ### end Alembic commands ###
