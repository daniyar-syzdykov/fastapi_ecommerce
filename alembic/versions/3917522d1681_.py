"""empty message

Revision ID: 3917522d1681
Revises: 
Create Date: 2022-10-04 12:35:12.196713

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
import uuid


# revision identifiers, used by Alembic.
revision = '3917522d1681'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('customers', sa.Column('uuid', UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()")))


def downgrade() -> None:
    pass
