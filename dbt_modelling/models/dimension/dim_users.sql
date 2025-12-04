with combined as (
    select
        us.user_id,
        concat(us.first_name, ' ', us.last_name) as full_name,
        us.email,
        cast(us.signup_date as timestamp(3)) as joined_date,
        lower(rg.region_name) as region,
        lower(pl.plan_name) as subscription_plan,
        lower(rf.source_name) as referral_source,
        cast(us.valid_from as timestamp(3)) as valid_from,
        cast(us.valid_to as timestamp(3)) as valid_to
    from {{ ref('stg_users') }} us
    left join {{ ref('stg_plans') }} pl on us.plan_id = pl.plan_id
    left join {{ ref('stg_regions') }} rg on us.region_id = rg.region_id
    left join {{ ref('stg_referrals') }} rf on us.referral_source_id = rf.referral_source_id
)
select * from combined 