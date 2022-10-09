"""empty message

Revision ID: 3917522d1681
Revises: 
Create Date: 2022-10-04 12:35:12.196713

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3917522d1681'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('customers', sa.Column('is_admin', sa.Boolean(), default=False))
    op.add_column('customers', sa.Column('is_active', sa.Boolean(), default=True))


def downgrade() -> None:
    pass
