with dim_usages as (
    select 
        {{ adapter.quote("usage_id") }},
        {{ adapter.quote("user_id") }},
        {{ adapter.quote("plan_id") }},
        {{ adapter.quote("usage_date") }},
        {{ adapter.quote("actions_performed") }},
        {{ adapter.quote("active_minutes") }},
        {{ adapter.quote("api_calls") }}

    from {{ ref('stg_usages') }}
)

select * from dim_usages