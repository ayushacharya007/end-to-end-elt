with fct_usages as(
    select 
        usage_date,
        user_id,
        sum(active_minutes) as total_active_minutes,
        sum(api_calls) as total_api_calls,
        sum(actions_performed) as total_actions_performed,
        sum(storage_used_mb) as total_storage_used_mb,
        count(user_id) as session_count
    from {{ ref('dim_usages') }}
    group by 
        usage_date,
        user_id
)

select * from fct_usages

