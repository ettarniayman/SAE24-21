"""add program_id and post_id to medias

Revision ID: a1b2c3d4e5f6
Revises: 9f7d150589f4
Create Date: 2026-06-18 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a1b2c3d4e5f6'
down_revision = '9f7d150589f4'
branch_labels = None
depends_on = None


def upgrade():
    # No-op si les colonnes existent deja (cas standard : base initialisee via
    # database/schema/schema.sql qui les definit deja).
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    columns = [c['name'] for c in inspector.get_columns('medias')]

    if 'program_id' not in columns:
        with op.batch_alter_table('medias', schema=None) as batch_op:
            batch_op.add_column(sa.Column('program_id', sa.Integer(), nullable=True))
            batch_op.create_foreign_key(
                'fk_medias_program_id', 'travel_programs', ['program_id'], ['id'], ondelete='SET NULL'
            )
            batch_op.create_index('idx_media_program', ['program_id'])

    if 'post_id' not in columns:
        with op.batch_alter_table('medias', schema=None) as batch_op:
            batch_op.add_column(sa.Column('post_id', sa.Integer(), nullable=True))
            batch_op.create_foreign_key(
                'fk_medias_post_id', 'blog_posts', ['post_id'], ['id'], ondelete='SET NULL'
            )
            batch_op.create_index('idx_media_post', ['post_id'])


def downgrade():
    with op.batch_alter_table('medias', schema=None) as batch_op:
        batch_op.drop_constraint('fk_medias_post_id', type_='foreignkey')
        batch_op.drop_index('idx_media_post')
        batch_op.drop_column('post_id')
        batch_op.drop_constraint('fk_medias_program_id', type_='foreignkey')
        batch_op.drop_index('idx_media_program')
        batch_op.drop_column('program_id')
