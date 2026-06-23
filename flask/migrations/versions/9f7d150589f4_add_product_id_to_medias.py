"""add product_id to medias

Revision ID: 9f7d150589f4
Revises: 36b123c35a1b
Create Date: 2026-06-18 08:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9f7d150589f4'
down_revision = '36b123c35a1b'
branch_labels = None
depends_on = None


def upgrade():
    # No-op si la colonne existe deja (cas standard : base initialisee via
    # database/schema/schema.sql qui la definit deja).
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    columns = [c['name'] for c in inspector.get_columns('medias')]

    if 'product_id' not in columns:
        with op.batch_alter_table('medias', schema=None) as batch_op:
            batch_op.add_column(sa.Column('product_id', sa.Integer(), nullable=True))
            batch_op.create_foreign_key(
                'fk_medias_product_id', 'shop_products', ['product_id'], ['id'], ondelete='SET NULL'
            )


def downgrade():
    with op.batch_alter_table('medias', schema=None) as batch_op:
        batch_op.drop_constraint('fk_medias_product_id', type_='foreignkey')
        batch_op.drop_column('product_id')
