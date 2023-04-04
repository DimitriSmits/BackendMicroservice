"""initial migration

Revision ID: b455eda5c320
Revises: 
Create Date: 2022-08-27 12:29:19.292779

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b455eda5c320'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('clusters',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('parent_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('is_approved', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['parent_id'], ['clusters.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_clusters_id'), 'clusters', ['id'], unique=False)
    op.create_table('features',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_features_id'), 'features', ['id'], unique=False)
    op.create_table('products',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('code', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('code')
    )
    op.create_index(op.f('ix_products_id'), 'products', ['id'], unique=False)
    op.create_table('cluster_features',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('cluster_id', sa.Integer(), nullable=False),
    sa.Column('feature_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['cluster_id'], ['clusters.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['feature_id'], ['features.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_cluster_features_cluster_id'), 'cluster_features', ['cluster_id'], unique=False)
    op.create_index(op.f('ix_cluster_features_id'), 'cluster_features', ['id'], unique=False)
    op.create_table('cluster_products',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('cluster_id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('probability', sa.Numeric(), nullable=False),
    sa.ForeignKeyConstraint(['cluster_id'], ['clusters.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('product_id')
    )
    op.create_index(op.f('ix_cluster_products_id'), 'cluster_products', ['id'], unique=False)
    op.create_table('feature_values',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('feature_id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('value', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['feature_id'], ['features.id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_feature_values_feature_id'), 'feature_values', ['feature_id'], unique=False)
    op.create_index(op.f('ix_feature_values_id'), 'feature_values', ['id'], unique=False)
    op.create_index(op.f('ix_feature_values_product_id'), 'feature_values', ['product_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_feature_values_product_id'), table_name='feature_values')
    op.drop_index(op.f('ix_feature_values_id'), table_name='feature_values')
    op.drop_index(op.f('ix_feature_values_feature_id'), table_name='feature_values')
    op.drop_table('feature_values')
    op.drop_index(op.f('ix_cluster_products_id'), table_name='cluster_products')
    op.drop_table('cluster_products')
    op.drop_index(op.f('ix_cluster_features_id'), table_name='cluster_features')
    op.drop_index(op.f('ix_cluster_features_cluster_id'), table_name='cluster_features')
    op.drop_table('cluster_features')
    op.drop_index(op.f('ix_products_id'), table_name='products')
    op.drop_table('products')
    op.drop_index(op.f('ix_features_id'), table_name='features')
    op.drop_table('features')
    op.drop_index(op.f('ix_clusters_id'), table_name='clusters')
    op.drop_table('clusters')
    # ### end Alembic commands ###
