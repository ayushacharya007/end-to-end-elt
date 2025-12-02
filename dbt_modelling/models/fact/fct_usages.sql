with fct_usages as(
    select 
        du.usage_date,
        du.user_id,
        du.actions_performed as total_actions,
        du.api_calls as total_api_calls,
        du.storage_used_mb as total_storage_used_mb,
        du.active_minutes as total_active_minutes,
        {# count of occurance of each user on same date #}
        count(du.user_id) as session_count

    from {{ ref('dim_usages') }} as du

    group by 
        du.usage_date,
        du.user_id
)

select * from fct_usages
limit 10