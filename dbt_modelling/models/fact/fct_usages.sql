with fct_usages as(
    select 
        usage_date,
        user_id,
        plan_id,
        sum(active_minutes) as total_active_minutes,
        sum(api_calls) as total_api_calls,
        sum(actions_performed) as total_actions_performed,
        round(sum(storage_used_mb), 2) as total_storage_used_mb,
        count(*) as session_count
    from {{ ref('dim_usages') }}
    group by 1, 2, 3
)

select * from fct_usages

