with fct_subscriptions as (
    select
        ds.user_id,
        ds.plan_id,
        sum(dp.monthly_fee) as total_revenue
    from {{ ref('dim_subscriptions') }} ds
    join {{ ref('dim_plans') }} dp
        on ds.plan_id = dp.plan_id
    group by 1, 2
)

select * from fct_subscriptions