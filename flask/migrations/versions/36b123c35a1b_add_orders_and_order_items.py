"""add orders and order_items tables

Revision ID: 36b123c35a1b
Revises: 7cebc0d7a827
Create Date: 2026-06-17 19:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '36b123c35a1b'
down_revision = '7cebc0d7a827'
branch_labels = None
depends_on = None


def upgrade():
    # No-op si les tables existent deja (cas standard : base initialisee via
    # database/schema/schema.sql qui les definit deja). Cree les tables seulement
    # si elles sont absentes, pour les environnements qui appliquent les
    # migrations Alembic sans repartir d'un schema.sql frais.
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    existing_tables = inspector.get_table_names()

    if 'orders' not in existing_tables:
        op.create_table(
            'orders',
            sa.Column('id', sa.Integer(), primary_key=True),
            sa.Column('reference', sa.String(length=20), nullable=False),
            sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='SET NULL'), nullable=True),
            sa.Column('first_name', sa.String(length=80), nullable=False),
            sa.Column('last_name', sa.String(length=80), nullable=False),
            sa.Column('email', sa.String(length=200), nullable=False),
            sa.Column('phone', sa.String(length=30), nullable=True),
            sa.Column('billing_address', sa.Text(), nullable=True),
            sa.Column('status', sa.String(length=20), nullable=False, server_default='pending'),
            sa.Column('payment_status', sa.String(length=20), nullable=False, server_default='pending'),
            sa.Column('subtotal', sa.Numeric(12, 2), nullable=False, server_default='0'),
            sa.Column('total', sa.Numeric(12, 2), nullable=False, server_default='0'),
            sa.Column('currency', sa.String(length=3), nullable=False, server_default='EUR'),
            sa.Column('notes', sa.Text(), nullable=True),
            sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
            sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
            sa.UniqueConstraint('reference'),
        )
        op.create_index('idx_orders_user', 'orders', ['user_id'])
        op.create_index('idx_orders_status', 'orders', ['status'])

    if 'order_items' not in existing_tables:
        op.create_table(
            'order_items',
            sa.Column('id', sa.Integer(), primary_key=True),
            sa.Column('order_id', sa.Integer(), sa.ForeignKey('orders.id', ondelete='CASCADE'), nullable=False),
            sa.Column('item_type', sa.String(length=20), nullable=False),
            sa.Column('program_id', sa.Integer(), sa.ForeignKey('travel_programs.id', ondelete='SET NULL'), nullable=True),
            sa.Column('product_id', sa.Integer(), sa.ForeignKey('shop_products.id', ondelete='SET NULL'), nullable=True),
            sa.Column('quantity', sa.Integer(), nullable=False, server_default='1'),
            sa.Column('unit_price', sa.Numeric(12, 2), nullable=False),
            sa.Column('departure_date', sa.Date(), nullable=True),
            sa.Column('participants', sa.Integer(), nullable=True),
            sa.Column('subtotal', sa.Numeric(12, 2), nullable=False),
            sa.CheckConstraint(
                "(item_type = 'program' AND program_id IS NOT NULL AND product_id IS NULL) OR "
                "(item_type = 'product' AND product_id IS NOT NULL AND program_id IS NULL)",
                name='chk_order_item_type',
            ),
        )
        op.create_index('idx_order_items_order', 'order_items', ['order_id'])


def downgrade():
    op.drop_index('idx_order_items_order', table_name='order_items')
    op.drop_table('order_items')
    op.drop_index('idx_orders_status', table_name='orders')
    op.drop_index('idx_orders_user', table_name='orders')
    op.drop_table('orders')
