"""Create initial tables

Revision ID: 0c331812bb4b
Revises: 
Create Date: 2025-05-21 10:18:33.090535

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0c331812bb4b'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('job_requests',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('request_id', sa.String(), nullable=False),
    sa.Column('payload', sa.JSON(), nullable=False),
    sa.Column('worker_id', sa.Integer(), nullable=True),
    sa.Column('status', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('processed_at', sa.DateTime(), nullable=True),
    sa.Column('result', sa.JSON(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_job_requests_id'), 'job_requests', ['id'], unique=False)
    op.create_index(op.f('ix_job_requests_request_id'), 'job_requests', ['request_id'], unique=True)
    op.create_table('workers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('status', sa.Enum('AVAILABLE', 'BUSY', name='workerstatus'), nullable=True),
    sa.Column('last_heartbeat', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_workers_id'), 'workers', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_workers_id'), table_name='workers')
    op.drop_table('workers')
    op.drop_index(op.f('ix_job_requests_request_id'), table_name='job_requests')
    op.drop_index(op.f('ix_job_requests_id'), table_name='job_requests')
    op.drop_table('job_requests')
    # ### end Alembic commands ###
