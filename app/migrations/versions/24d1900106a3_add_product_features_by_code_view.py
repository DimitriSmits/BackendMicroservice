"""Add product-features-by-code view

Revision ID: 24d1900106a3
Revises: c7ad5e3cc0e3
Create Date: 2022-10-26 07:39:07.662352

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '24d1900106a3'
down_revision = 'c7ad5e3cc0e3'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        '''
        create materialized view product_features_by_code as (
            select
                feature_values.product_id,
                json_object_agg(features.code, feature_values.value) as feature_values
            from
                feature_values
                left join features on features.id = feature_values.feature_id
            group by
                feature_values.product_id
        );
        '''
    )

def downgrade() -> None:
    op.execute('drop materialized view product_features_by_code;')
