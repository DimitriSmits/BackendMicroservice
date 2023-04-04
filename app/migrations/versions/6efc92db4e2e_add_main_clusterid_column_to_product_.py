"""add_main_clusterid_column_to_product_table

Revision ID: 6efc92db4e2e
Revises: 5e6e0577205d
Create Date: 2022-10-25 09:53:17.165678

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6efc92db4e2e'
down_revision = '5e6e0577205d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('products', sa.Column('main_cluster_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'products', 'clusters', ['main_cluster_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'products', type_='foreignkey')
    op.drop_column('products', 'main_cluster_id')
    # ### end Alembic commands ###
