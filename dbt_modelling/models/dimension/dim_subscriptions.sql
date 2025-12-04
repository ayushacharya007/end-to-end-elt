with combined as (
    select
        ss.subscription_id,
        ss.user_id,
        lower(sp.plan_name) as plan_name,
        lower(spay.method_name) as payment_method,
        ss.start_date as start_date,
        ss.end_date as end_date,
        lower(ss.status) as status,
        cast(ss.valid_from as timestamp(3)) as valid_from,
        cast(ss.valid_to as timestamp(3)) as valid_to
    from {{ ref('stg_subscriptions') }} ss
    left join {{ ref('stg_users') }} su on ss.user_id = su.user_id
    left join {{ ref('stg_plans') }} sp on ss.plan_id = sp.plan_id
    left join {{ ref('stg_payment_methods') }} spay on ss.payment_method_id = spay.payment_method_id
)
select * from combined
limit 10