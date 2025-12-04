with combined as (
    select 
        sp.plan_id,
        lower(sp.plan_name) as plan_name,
        sp.monthly_fee,
        sp.max_users,
        sp.api_limit,
        sp.storage_limit_mb,
        sp.project_limit,
        lower(sf.feature_name) as feature_name
    from {{ ref('stg_plans') }} sp
    left join {{ ref('stg_features') }} sf on sp.plan_id = sf.plan_id
)
select * from combined