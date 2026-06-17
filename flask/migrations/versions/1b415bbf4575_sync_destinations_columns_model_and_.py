"""sync destinations columns model and schema

Revision ID: 1b415bbf4575
Revises: 
Create Date: 2026-06-16 23:10:12.025667

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1b415bbf4575'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # No-op: ces colonnes sont deja definies directement dans database/schema/schema.sql
    # (budget_low, budget_high, currency_local sur destinations ; medias.file_path nullable).
    # Cette migration reste dans l'historique pour ne pas casser la chaine de revisions,
    # mais n'execute plus de DDL pour eviter les erreurs "column already exists" au
    # premier "flask db upgrade" sur une base initialisee via docker-entrypoint-initdb.d.
    pass


def downgrade():
    pass
