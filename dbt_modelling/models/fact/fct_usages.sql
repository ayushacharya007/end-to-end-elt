with combined as (
    select 
        sug.usage_date,
        u.user_id,
        s.subscription_id,
        s.plan_name,
        sum(sug.actions_performed) as total_actions_performed,
        sum(sug.active_minutes) as total_active_minutes,
        sum(sug.api_calls) as total_api_calls,
        sum(sug.storage_used_mb) as total_storage_used_mb
    from {{ ref('stg_usages') }} sug
    left join {{ ref('dim_users') }} du on sug.user_id = du.user_id
    left join {{ ref('dim_subscriptions') }} ds on sug.subscription_id = ds.subscription_id
    group by 
        sug.usage_date,
        du.user_id,
        ds.subscription_id,
        ds.plan_name
)
select * from combined