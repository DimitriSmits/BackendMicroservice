"""Drop main_cluster_id column from products table

Revision ID: 615e677bc3ab
Revises: 24d1900106a3
Create Date: 2022-10-27 11:10:38.055749

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '615e677bc3ab'
down_revision = '24d1900106a3'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('products_main_cluster_id_fkey', 'products', type_='foreignkey')
    op.drop_column('products', 'main_cluster_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('products', sa.Column('main_cluster_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('products_main_cluster_id_fkey', 'products', 'clusters', ['main_cluster_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###
