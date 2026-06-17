"""add sort_order to destination_activities and program_destinations

Revision ID: 7cebc0d7a827
Revises: 1b415bbf4575
Create Date: 2026-06-17 14:10:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7cebc0d7a827'
down_revision = '1b415bbf4575'
branch_labels = None
depends_on = None


def upgrade():
    # No-op: sort_order est deja defini directement dans database/schema/schema.sql
    # pour destination_activities et program_destinations. Voir 1b415bbf4575 pour le
    # contexte (meme situation pour les colonnes destinations).
    pass


def downgrade():
    pass
