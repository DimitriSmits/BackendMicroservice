"""add views

Revision ID: 70d8b79b1008
Revises: b455eda5c320
Create Date: 2022-08-27 12:31:19.518315

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = '70d8b79b1008'
down_revision = 'b455eda5c320'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        '''
        create materialized view product_features as (
            select
                feature_values.product_id,
                json_object_agg(features.name, feature_values.value) as feature_values
            from
                feature_values
                left join features on features.id = feature_values.feature_id
            group by
                feature_values.product_id
        );
        '''
    )
    op.execute(
        '''
        create view cluster_ancestors as (
            with recursive cte as (
                    select
                        c1.id,
                        ARRAY[c1.id]::INTEGER[] as cluster_tree
                    from
                        clusters c1
                    where
                        c1.parent_id is null
                union	
                    select 
                        c2.id,
                        c2.parent_id || cte.cluster_tree
                    from
                        clusters c2
                    join cte on cte.id = c2.parent_id
            )
            select
                cte.*
            from 
                cte
        );
        '''
    )
    op.execute(
        '''
        create view product_features_cluster as (
            select
                products.*,
                coalesce(product_features.feature_values, '{}'::json) as feature_values,
                cluster_products.cluster_id,
                cluster_products.probability as cluster_probability,
                clusters.name as cluster_name,
                cluster_ancestors.cluster_tree
            from
                products
                left join product_features on product_features.product_id = products.id
                left join cluster_products on cluster_products.product_id = products.id
                left join clusters on clusters.id = cluster_products.cluster_id
                left join cluster_ancestors on cluster_ancestors.id = cluster_products.cluster_id
        );
        '''
    )
    op.execute(
        '''
        create view cluster_features_agg as (
            select
                cluster_features.cluster_id,
                array_agg(features.name) as features
            from
                cluster_features
                join features on features.id = cluster_features.feature_id
            group by
                cluster_features.cluster_id
        );
        '''
    )
    
    op.execute(
        '''
        create or replace view cluster_num_products as (
            select
                clusters.id as cluster_id,
                coalesce(num_products_per_cluster.number_of_products, 0) as number_of_products
            from
                clusters
                left join (
                    select
                        cluster_products.cluster_id,
                        count(cluster_products.cluster_id) AS number_of_products
                    from
                        cluster_products
                    group by
                        cluster_products.cluster_id
                ) num_products_per_cluster on num_products_per_cluster.cluster_id = clusters.id
            )
        ;
        '''
    )
    op.execute(
        '''
        create view cluster_features_num_products as (
            select
                clusters.*,
                coalesce(cluster_features_agg.features, '{}'::VARCHAR[]) as features,
                coalesce(cluster_num_products.number_of_products, 0) as number_of_products
            from
                clusters
            left join cluster_features_agg on cluster_features_agg.cluster_id = clusters.id
            left join cluster_num_products on cluster_num_products.cluster_id = clusters.id
        );
        '''
    )


def downgrade() -> None:
    op.execute('drop view if exists cluster_features_num_products;')
    op.execute('drop view if exists cluster_num_products;')
    op.execute('drop view if exists cluster_features_agg;')
    op.execute('drop view if exists product_features_cluster;')
    op.execute('drop view if exists cluster_ancestors;')
    op.execute('drop materialized view if exists product_features;')
