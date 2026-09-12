"""create_collector_profiles_table

Revision ID: c1a2b3d4e5f6
Revises: be0b49cc4799
Create Date: 2026-09-12 10:46:15.451228

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c1a2b3d4e5f6'
down_revision: Union[str, Sequence[str], None] = 'be0b49cc4799'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('collector_profiles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('whatsapp_number', sa.String(), nullable=False),
    sa.Column('display_name', sa.String(), nullable=True),
    sa.Column('area', sa.String(), nullable=True),
    sa.Column('latitude', sa.Float(), nullable=False),
    sa.Column('longitude', sa.Float(), nullable=False),
    sa.Column('active', sa.Boolean(), nullable=False, server_default=sa.true()),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id')
    )
    op.create_index(op.f('ix_collector_profiles_id'), 'collector_profiles', ['id'], unique=False)
    op.create_index(op.f('ix_collector_profiles_user_id'), 'collector_profiles', ['user_id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_collector_profiles_user_id'), table_name='collector_profiles')
    op.drop_index(op.f('ix_collector_profiles_id'), table_name='collector_profiles')
    op.drop_table('collector_profiles')
