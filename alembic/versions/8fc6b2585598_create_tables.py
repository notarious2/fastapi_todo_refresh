"""create tables

Revision ID: 8fc6b2585598
Revises: c60f4695886d
Create Date: 2022-11-15 09:40:34.985509

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8fc6b2585598'
down_revision = 'c60f4695886d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('user_id', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('password', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('user_id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_user_id'), 'user', ['user_id'], unique=False)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.create_table('task',
    sa.Column('task_id', sa.String(), nullable=False),
    sa.Column('priority', sa.Integer(), nullable=True),
    sa.Column('date', sa.Date(), nullable=True),
    sa.Column('text', sa.String(), nullable=False),
    sa.Column('completed', sa.Boolean(), nullable=True),
    sa.Column('user_id', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], ),
    sa.PrimaryKeyConstraint('task_id')
    )
    op.create_index(op.f('ix_task_task_id'), 'task', ['task_id'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_task_task_id'), table_name='task')
    op.drop_table('task')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_user_id'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###
