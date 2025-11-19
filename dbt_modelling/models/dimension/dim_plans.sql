with dim_plans as (
    select 
        {{ adapter.quote("plan_id") }},
        {{ adapter.quote("plan_name") }},
        {{ adapter.quote("monthly_fee") }},
        {{ adapter.quote("max_users") }},
        {{ adapter.quote("features") }}

    from {{ ref('stg_plans') }}
)

select * from dim_plans