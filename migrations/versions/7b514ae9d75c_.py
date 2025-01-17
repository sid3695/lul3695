"""empty message

Revision ID: 7b514ae9d75c
Revises: 
Create Date: 2019-01-28 00:54:20.097598

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7b514ae9d75c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('username', sa.String(length=40), nullable=False),
    sa.Column('emp_id', sa.Integer(), nullable=False),
    sa.Column('first_login', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('emp_id')
    )
    op.create_table('date',
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('day_id', sa.Integer(), nullable=False),
    sa.Column('emp_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['emp_id'], ['user.emp_id'], ),
    sa.PrimaryKeyConstraint('day_id')
    )
    op.create_table('devices',
    sa.Column('devicename', sa.String(length=20), nullable=False),
    sa.Column('device_id', sa.Integer(), nullable=False),
    sa.Column('emp_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['emp_id'], ['user.emp_id'], ),
    sa.PrimaryKeyConstraint('device_id')
    )
    op.create_table('events',
    sa.Column('event_id', sa.Integer(), nullable=False),
    sa.Column('action', sa.String(length=10), nullable=False),
    sa.Column('value', sa.String(length=10), nullable=False),
    sa.Column('devicename', sa.String(length=20), nullable=False),
    sa.Column('timestamp', sa.Time(), nullable=False),
    sa.Column('day_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['day_id'], ['date.day_id'], ),
    sa.PrimaryKeyConstraint('event_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('events')
    op.drop_table('devices')
    op.drop_table('date')
    op.drop_table('user')
    # ### end Alembic commands ###
