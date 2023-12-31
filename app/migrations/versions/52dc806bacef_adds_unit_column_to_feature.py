"""Adds unit column to Feature

Revision ID: 52dc806bacef
Revises: 37072281c42b
Create Date: 2022-10-05 14:47:02.631694

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = '52dc806bacef'
down_revision = '37072281c42b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('feature_options', sa.Column('feature_id', sa.Integer(), nullable=False))
    op.drop_index('ix_feature_options_cluster_id', table_name='feature_options')
    op.create_index(op.f('ix_feature_options_feature_id'), 'feature_options', ['feature_id'], unique=False)
    op.drop_constraint('feature_options_cluster_id_fkey', 'feature_options', type_='foreignkey')
    op.create_foreign_key(None, 'feature_options', 'features', ['feature_id'], ['id'], ondelete='CASCADE')
    op.drop_column('feature_options', 'cluster_id')

    feature_unit_enum = postgresql.ENUM('G', 'MM', 'M', 'L', 'KG', 'ML', 'INCH', name='featureunit')
    feature_unit_enum.create(op.get_bind())
    op.add_column('features', sa.Column('unit', feature_unit_enum, nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('features', 'unit')
    op.add_column('feature_options', sa.Column('cluster_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'feature_options', type_='foreignkey')
    op.create_foreign_key('feature_options_cluster_id_fkey', 'feature_options', 'features', ['cluster_id'], ['id'], ondelete='CASCADE')
    op.drop_index(op.f('ix_feature_options_feature_id'), table_name='feature_options')
    op.create_index('ix_feature_options_cluster_id', 'feature_options', ['cluster_id'], unique=False)
    op.drop_column('feature_options', 'feature_id')
    # ### end Alembic commands ###
