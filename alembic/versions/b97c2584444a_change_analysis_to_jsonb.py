"""change analysis to jsonb

Revision ID: b97c2584444a
Revises: b8dd4df63389
Create Date: 2026-07-22 15:28:08.659726

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'b97c2584444a'
down_revision: Union[str, Sequence[str], None] = 'b8dd4df63389'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.execute("""
        ALTER TABLE resumes
        ALTER COLUMN analysis
        TYPE JSONB
        USING analysis::jsonb
    """)


def downgrade():
    op.execute("""
        ALTER TABLE resumes
        ALTER COLUMN analysis
        TYPE TEXT
        USING analysis::text
    """)
